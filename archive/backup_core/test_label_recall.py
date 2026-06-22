"""
Test de recuperación de imagen a partir de label semántico.

Flujo:
  label (texto)
    → fastText vector → quantize_binary(v, 16) → v_label_q
    → M_dom.recall_from_left(v_label_q) → recalled_q  (cuantizado en [0,31]^64)
    → dequantize con g_min/g_max globales → v_latent  (espacio real del encoder)
    → decoder → imagen [0,1]

La función dequantize() por defecto usa vmin=-1, vmax=1, lo que es incorrecto
para el espacio latente (rango real ≈ [-16, +20] por dimension).
Aqui usamos la dequantizacion correcta con latent_global_stats.json.

Pruebas:
  1. Labels propios de cada dominio
  2. Queries multi-token
  3. Cross-domain (label de X → agente de Y)

Salida: results/label_recall/
"""
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torchvision import transforms

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from quantizer import quantize_binary
from stage6_interaction import (
    CLASSES, AGENT_LIST, MODELS_DIR,
    get_nlp, load_all_vectors, tokenize_query, get_fasttext_vector, M_LABEL,
)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_DIR = ROOT / "results" / "label_recall"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
Q_LATENT = 32   # niveles de cuantización del latente (debe coincidir con stage5)

# ──────────────────────────────────────────────────────────────────
# Labels de prueba
# ──────────────────────────────────────────────────────────────────

TEST_LABELS = {
    "apple": ["pome", "core", "seeds", "delicious", "fruit", "round"],
    "horse": ["mane", "hooves", "equine", "saddle", "racing", "pony"],
    "car":   ["vehicle", "automobile", "wheels", "driver", "crash", "seat"],
}

MULTITOKEN_QUERIES = [
    ("round red fruit",            "apple"),
    ("grows on fruit trees",       "apple"),
    ("animal with a mane",         "horse"),
    ("large powerful mammal",      "horse"),
    ("fast vehicle with wheels",   "car"),
    ("machine for transportation", "car"),
]

CROSS_DOMAIN_TESTS = [
    ("mane",       "horse", "apple"),
    ("hooves",     "horse", "car"),
    ("vehicle",    "car",   "apple"),
    ("automobile", "car",   "horse"),
    ("core",       "apple", "horse"),
    ("pome",       "apple", "car"),
]

DOMAIN_COLORS = {"apple": "#e74c3c", "horse": "#2980b9", "car": "#27ae60"}


# ──────────────────────────────────────────────────────────────────
# Carga de modelos y stats
# ──────────────────────────────────────────────────────────────────

def load_decoder():
    from stage2_encoder import Decoder
    dec = Decoder().to(DEVICE)
    dec.load_state_dict(torch.load(MODELS_DIR / "decoder.pt", map_location=DEVICE))
    dec.eval()
    return dec


def load_mdoms() -> dict:
    mdoms = {}
    for cls in CLASSES:
        with open(MODELS_DIR / f"mem_dom_{cls}.pkl", "rb") as f:
            mdoms[cls] = pickle.load(f)
    return mdoms


def load_global_stats():
    """Carga g_min y g_max (shape [64]) para dequantizar el latente correctamente."""
    stats = json.loads((MODELS_DIR / "latent_global_stats.json").read_text())
    return np.array(stats["global_min"]), np.array(stats["global_max"])


def dequantize_latent(q_vals: np.ndarray, g_min: np.ndarray,
                      g_max: np.ndarray) -> np.ndarray:
    """
    Inversa de quantize_latent_global.
    q_vals: [0, Q-1]^64  →  v_latent: [g_min, g_max]^64
    """
    v_norm = q_vals.astype(float) / (Q_LATENT - 1)        # [0, 1]
    return (v_norm * (g_max - g_min) + g_min).astype(np.float32)


def load_real_images() -> dict:
    """Una imagen real de referencia por dominio (sin normalizar, en [0,1])."""
    splits_path = ROOT / "data" / "eth80" / "splits.json"
    splits = json.loads(splits_path.read_text())
    to_tensor = transforms.ToTensor()
    real_imgs = {}
    for cls in CLASSES:
        path = splits[cls]["train"][0]
        img = Image.open(path).convert("RGB").resize((128, 128))
        real_imgs[cls] = to_tensor(img)   # [0, 1], shape (3, 128, 128)
    return real_imgs


# ──────────────────────────────────────────────────────────────────
# Core recall (con dequantización correcta)
# ──────────────────────────────────────────────────────────────────

def recall_word(word: str, agent_cls: str, mdoms: dict, vectors_cache: dict,
                decoder, g_min, g_max) -> dict:
    """Label de una palabra → imagen."""
    v   = get_fasttext_vector(word, vectors_cache)
    v_q = quantize_binary(v, M_LABEL)

    recalled_q, recognized, weight = mdoms[agent_cls].recall_from_left(v_q)

    img = None
    if recognized:
        v_latent = dequantize_latent(recalled_q, g_min, g_max)
        z = torch.tensor(v_latent).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            img = decoder(z)[0].cpu()

    return {"word": word, "agent": agent_cls,
            "recognized": recognized, "weight": weight, "image": img}


def recall_query(query: str, agent_cls: str, mdoms: dict, vectors_cache: dict,
                 decoder, g_min, g_max, nlp) -> dict:
    """Query multi-token → imagen (usa el primer token reconocido)."""
    tokens = tokenize_query(query, nlp)
    if not tokens:
        return {"query": query, "agent": agent_cls, "tokens": [],
                "n_recog": 0, "weight": 0.0, "image": None}

    total_w, n_recog, best_img = 0.0, 0, None
    for tok in tokens:
        v   = get_fasttext_vector(tok, vectors_cache)
        v_q = quantize_binary(v, M_LABEL)
        recalled_q, recognized, w = mdoms[agent_cls].recall_from_left(v_q)
        total_w += w
        n_recog += int(recognized)
        if recognized and best_img is None:
            v_latent = dequantize_latent(recalled_q, g_min, g_max)
            z = torch.tensor(v_latent).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                best_img = decoder(z)[0].cpu()

    return {"query": query, "agent": agent_cls, "tokens": tokens,
            "n_recog": n_recog, "weight": total_w / max(len(tokens), 1),
            "image": best_img}


# ──────────────────────────────────────────────────────────────────
# Helpers de dibujo
# ──────────────────────────────────────────────────────────────────

def _draw_img_cell(ax, img, title: str, recognized: bool, weight: float,
                   border_color: str = None):
    if img is not None:
        np_img = img.permute(1, 2, 0).numpy()
        ax.imshow(np.clip(np_img, 0, 1), interpolation="bilinear")
    else:
        ax.set_facecolor("#eeeeee")
        ax.text(0.5, 0.5, "No\nreconocido", ha="center", va="center",
                transform=ax.transAxes, fontsize=8, color="gray")

    status = "OK" if recognized else "FALLO"
    txt_color = "#2ecc71" if recognized else "#e74c3c"
    ax.set_title(f"{title}\nw={weight:.0f}  [{status}]",
                 fontsize=7.5, color=txt_color, fontweight="bold", pad=3)
    ax.axis("off")

    if border_color:
        for sp in ax.spines.values():
            sp.set_visible(True)
            sp.set_edgecolor(border_color)
            sp.set_linewidth(3)


def _ref_cell(ax, img_tensor, cls: str):
    ax.imshow(img_tensor.permute(1, 2, 0).numpy())
    ax.set_title(f"ETH-80\n[{cls}]", fontsize=8, fontweight="bold",
                 color=DOMAIN_COLORS[cls], pad=3)
    ax.axis("off")
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_edgecolor(DOMAIN_COLORS[cls])
        sp.set_linewidth(4)


# ──────────────────────────────────────────────────────────────────
# Plot 1: Labels propios → imagen recuperada
# ──────────────────────────────────────────────────────────────────

def plot_own_domain(mdoms, vectors_cache, decoder, g_min, g_max, real_imgs):
    n_lbls = max(len(v) for v in TEST_LABELS.values())
    n_cols = 1 + n_lbls   # col 0 = ref, cols 1.. = labels
    fig, axes = plt.subplots(3, n_cols, figsize=(2.6 * n_cols, 3.8 * 3))

    for row, cls in enumerate(CLASSES):
        _ref_cell(axes[row][0], real_imgs[cls], cls)

        for ci, word in enumerate(TEST_LABELS[cls]):
            ax = axes[row][ci + 1]
            res = recall_word(word, cls, mdoms, vectors_cache,
                              decoder, g_min, g_max)
            bc = DOMAIN_COLORS[cls] if res["recognized"] else "#e74c3c"
            _draw_img_cell(ax, res["image"], f'"{word}"',
                           res["recognized"], res["weight"], bc)

    plt.suptitle(
        "Recuperacion label -> imagen (M_dom)\n"
        "Col. izq = imagen real ETH-80 de referencia",
        fontsize=12, fontweight="bold", y=1.01)
    plt.tight_layout()
    out = RESULTS_DIR / "recall_own_domain.png"
    plt.savefig(out, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {out.name}")


# ──────────────────────────────────────────────────────────────────
# Plot 2: Multi-token queries
# ──────────────────────────────────────────────────────────────────

def plot_multitoken(mdoms, vectors_cache, decoder, g_min, g_max, real_imgs, nlp):
    nq = len(MULTITOKEN_QUERIES)
    fig, axes = plt.subplots(nq, 3, figsize=(11, 3.0 * nq))

    for i, (query, true_cls) in enumerate(MULTITOKEN_QUERIES):
        row = axes[i]
        wrong_cls = CLASSES[(CLASSES.index(true_cls) + 1) % 3]

        # Columna 0: imagen real
        _ref_cell(row[0], real_imgs[true_cls], true_cls)
        row[0].set_ylabel(f"Q{i+1}", rotation=0, labelpad=45,
                          fontsize=8, va="center")

        # Columna 1: agente correcto
        r_ok = recall_query(query, true_cls, mdoms, vectors_cache,
                             decoder, g_min, g_max, nlp)
        toks_str = " | ".join(r_ok["tokens"])
        _draw_img_cell(row[1], r_ok["image"],
                       f'"{query}"\ntokens: [{toks_str}]',
                       r_ok["n_recog"] > 0, r_ok["weight"],
                       DOMAIN_COLORS[true_cls])

        # Columna 2: agente incorrecto (comparación)
        r_bad = recall_query(query, wrong_cls, mdoms, vectors_cache,
                              decoder, g_min, g_max, nlp)
        _draw_img_cell(row[2], r_bad["image"],
                       f"Agente incorrecto [{wrong_cls}]",
                       r_bad["n_recog"] > 0, r_bad["weight"])

    col_labels = ["Imagen real\n(referencia)",
                  "Recall: agente CORRECTO",
                  "Recall: agente INCORRECTO"]
    for ax, lbl in zip(axes[0], col_labels):
        ax.set_title(lbl, fontsize=9, fontweight="bold", pad=12)

    plt.suptitle("Recuperacion multi-token: agente correcto vs incorrecto",
                 fontsize=12, fontweight="bold", y=1.01)
    plt.tight_layout()
    out = RESULTS_DIR / "recall_multitoken.png"
    plt.savefig(out, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {out.name}")


# ──────────────────────────────────────────────────────────────────
# Plot 3: Cross-domain
# ──────────────────────────────────────────────────────────────────

def plot_cross_domain(mdoms, vectors_cache, decoder, g_min, g_max, real_imgs):
    n = len(CROSS_DOMAIN_TESTS)
    fig, axes = plt.subplots(n, 4, figsize=(14, 3.0 * n))

    for i, (word, src_cls, wrong_cls) in enumerate(CROSS_DOMAIN_TESTS):
        row = axes[i]

        # Col 0: imagen real del dominio fuente
        _ref_cell(row[0], real_imgs[src_cls], src_cls)

        # Col 1: recall correcto
        r_ok = recall_word(word, src_cls, mdoms, vectors_cache,
                           decoder, g_min, g_max)
        _draw_img_cell(row[1], r_ok["image"],
                       f'"{word}" -> [{src_cls}]\nCORRECTO',
                       r_ok["recognized"], r_ok["weight"],
                       DOMAIN_COLORS[src_cls])

        # Col 2: recall incorrecto
        r_bad = recall_word(word, wrong_cls, mdoms, vectors_cache,
                            decoder, g_min, g_max)
        _draw_img_cell(row[2], r_bad["image"],
                       f'"{word}" -> [{wrong_cls}]\nINCORRECTO',
                       r_bad["recognized"], r_bad["weight"])

        # Col 3: imagen real del agente incorrecto (referencia)
        _ref_cell(row[3], real_imgs[wrong_cls], wrong_cls)
        row[3].set_title(f"Real [{wrong_cls}]\n(NO deberia salir)",
                         fontsize=8, color="gray", style="italic", pad=3)
        row[3].axis("off")

    col_labels = ["Imagen real\n(origen)",
                  "Recall correcto\n(agente propio)",
                  "Recall incorrecto\n(agente ajeno)",
                  "Referencia\n(agente ajeno)"]
    for ax, lbl in zip(axes[0], col_labels):
        ax.set_title(lbl, fontsize=9, fontweight="bold", pad=12)

    plt.suptitle(
        "Cross-domain: label de dominio X enviado al agente Y\n"
        "Si OK=FALLO y peso=0 -> M_dom es especifico (bueno!)",
        fontsize=11, fontweight="bold", y=1.01)
    plt.tight_layout()
    out = RESULTS_DIR / "recall_cross_domain.png"
    plt.savefig(out, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"  Guardado: {out.name}")


# ──────────────────────────────────────────────────────────────────
# Resumen en consola
# ──────────────────────────────────────────────────────────────────

def print_summary(mdoms, vectors_cache, decoder, g_min, g_max, nlp):
    print("\n" + "="*65)
    print("RESUMEN: Label -> Imagen (recall desde M_dom)")
    print("="*65)

    print("\n[1] Labels propios (deben ser reconocidos con peso alto):")
    print(f"  {'Label':15s}  {'Agente':8s}  {'Recono.':10s}  {'Peso':>12s}")
    print(f"  {'-'*55}")
    for cls in CLASSES:
        for word in TEST_LABELS[cls]:
            r = recall_word(word, cls, mdoms, vectors_cache,
                            decoder, g_min, g_max)
            flag = "SI" if r["recognized"] else "NO"
            print(f"  {word:15s}  {cls:8s}  {flag:10s}  {r['weight']:12.1f}")

    print("\n[2] Multi-token queries:")
    print(f"  {'Query':35s}  {'Agente':8s}  {'Tokens':>12s}  {'Peso':>10s}")
    print(f"  {'-'*75}")
    for query, true_cls in MULTITOKEN_QUERIES:
        r = recall_query(query, true_cls, mdoms, vectors_cache,
                         decoder, g_min, g_max, nlp)
        print(f"  {query[:33]:35s}  {true_cls:8s}  "
              f"{r['n_recog']}/{len(r['tokens'])} tok  "
              f"{r['weight']:10.1f}")

    print("\n[3] Cross-domain (esperado: peso=0 / no reconocido):")
    print(f"  {'Label':12s}  {'Origen':8s}  {'Agente incorrecto':18s}  "
          f"{'Recono.':10s}  {'Peso':>10s}")
    print(f"  {'-'*70}")
    for word, src_cls, wrong_cls in CROSS_DOMAIN_TESTS:
        r = recall_word(word, wrong_cls, mdoms, vectors_cache,
                        decoder, g_min, g_max)
        flag = "SI (leak!)" if r["recognized"] else "NO (correcto)"
        print(f"  {word:12s}  {src_cls:8s}  {wrong_cls:18s}  "
              f"{flag:10s}  {r['weight']:10.1f}")


# ──────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────

def run():
    print("=== TEST DE RECUPERACION IMAGEN POR LABEL ===\n")

    print("Cargando modelos...")
    decoder       = load_decoder()
    mdoms         = load_mdoms()
    vectors_cache = load_all_vectors()
    g_min, g_max  = load_global_stats()
    nlp           = get_nlp()
    real_imgs     = load_real_images()
    print(f"  Latent range: dim0 in [{g_min[0]:.1f}, {g_max[0]:.1f}] "
          f"(rango real, NO [-1,1])")

    print("\nGenerando plots...")
    print("  [1/3] Labels propios por dominio...")
    plot_own_domain(mdoms, vectors_cache, decoder, g_min, g_max, real_imgs)

    print("  [2/3] Multi-token queries...")
    plot_multitoken(mdoms, vectors_cache, decoder, g_min, g_max, real_imgs, nlp)

    print("  [3/3] Cross-domain test...")
    plot_cross_domain(mdoms, vectors_cache, decoder, g_min, g_max, real_imgs)

    print_summary(mdoms, vectors_cache, decoder, g_min, g_max, nlp)

    print(f"\nResultados en: {RESULTS_DIR}")
    print("=== COMPLETADO ===")


if __name__ == "__main__":
    run()
