"""
Etapa 5 — Llenado de las memorias de dominio por agente.

Cada agente recibe tres memorias:
  mem_dom_{cls}.pkl    HeteroAssociativeMemory(300,16,64,32)  label <-> latente
  mem_dom_L_{cls}.pkl  HomoAssociativeMemory(300,16)          dominio label
  mem_dom_R_{cls}.pkl  HomoAssociativeMemory(64,32)           dominio latente

El llenado es por instancias (image-major): cada una de las N_FILL imagenes
reales —×4 variantes si FILL_AUGMENT (original + espejo + 2 rotaciones), el
valor vigente— entra a la memoria hetero, emparejada con el siguiente label
de la secuencia de labels expandida por frecuencia (800 registros/clase con
N_FILL=200). La abstraccion de la clase la construye la propia memoria al
acumular; ningun prototipo se calcula fuera de ella.

Las stats globales de cuantizacion del latente se calculan sobre el mismo
pool de imagenes que llena las memorias. Los latentes continuos del pool
se guardan en instance_latents_{cls}.json para reuso (p. ej. el ablation
reconstruye memorias curadas con el mismo protocolo).
"""
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import torch
from torchvision import transforms
from PIL import Image

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from hetero_memory import HeteroAssociativeMemory
from associative_memory import HomoAssociativeMemory
from quantizer import quantize_binary

CLASSES = ["apple", "car", "cow", "cup", "dog", "horse", "pear", "tomato"]
N, M, P, Q = 300, 16, 64, 32
# N_FILL=200 deja train[200:328] libre para las interacciones visuales de
# stage7. El llenado se enriquece por augmentación (4x por imagen), no
# consumiendo más imágenes.
N_FILL = 200
FILL_AUGMENT = True      # augmentar cada imagen (espejo + rotaciones) al llenar
FILL_AUG_ANGLES = (-12, 12)
MODELS_DIR = ROOT / "models"
DATA_DIR = ROOT / "data" / "eth80"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

IMG_TRANSFORM = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def load_encoder():
    from stage2_encoder import load_models
    encoder, _, _ = load_models()
    return encoder


def _augment_variants(img):
    """Variantes por imagen para enriquecer el llenado sin datos nuevos:
    original + espejo horizontal + dos rotaciones suaves. Amplía la cobertura
    del espacio latente de la clase (menos rechazo por containment) sin salir
    del propio dataset. Es solo más percepción registrada en la MAE, no un truco."""
    variants = [img, img.transpose(Image.FLIP_LEFT_RIGHT)]
    for angle in FILL_AUG_ANGLES:
        variants.append(img.rotate(angle, resample=Image.BILINEAR))
    return variants


def get_instance_latents(encoder, cls: str, n: int = N_FILL) -> list:
    """Codifica las primeras n imagenes de entrenamiento de la clase (con
    augmentacion si FILL_AUGMENT)."""
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    paths = splits[cls]["train"][:n]
    zs = []
    encoder.eval()
    with torch.no_grad():
        for p in paths:
            img = Image.open(p).convert("RGB").resize((128, 128))
            variants = _augment_variants(img) if FILL_AUGMENT else [img]
            for v in variants:
                img_t = IMG_TRANSFORM(v).unsqueeze(0).to(DEVICE)
                zs.append(encoder(img_t).cpu().numpy()[0])
    return zs


def compute_global_latent_stats(encoder, latents_by_cls: dict = None) -> tuple:
    """Min/max global por dimension sobre el pool de llenado, con margen
    del 10% contra efectos de borde."""
    stats_path = MODELS_DIR / "latent_global_stats.json"
    if stats_path.exists():
        s = json.loads(stats_path.read_text())
        return np.array(s["global_min"]), np.array(s["global_max"])

    print(f"  Calculando stats globales sobre {N_FILL} imagenes/clase...")
    all_zs = []
    if latents_by_cls is not None:
        for cls in CLASSES:
            all_zs.extend(latents_by_cls[cls])
    else:
        for cls in CLASSES:
            all_zs.extend(get_instance_latents(encoder, cls, N_FILL))
    all_zs = np.stack(all_zs)
    g_min = all_zs.min(axis=0)
    g_max = all_zs.max(axis=0)
    margin = 0.1 * (g_max - g_min)
    g_min -= margin
    g_max += margin
    stats_path.write_text(json.dumps({
        "global_min": g_min.tolist(),
        "global_max": g_max.tolist(),
    }))
    return g_min, g_max


def quantize_latent_global(v: np.ndarray, g_min: np.ndarray,
                           g_max: np.ndarray, q: int) -> np.ndarray:
    rng = g_max - g_min
    rng = np.where(rng == 0, 1e-8, rng)
    v_norm = np.clip((v - g_min) / rng, 0.0, 1.0)
    q_vals = np.floor(v_norm * q).astype(np.int32)
    return np.clip(q_vals, 0, q - 1)


def build_label_sequence(cls: str) -> list:
    """Labels de la clase expandidos por frecuencia, ya cuantizados.
    El orden de insercion es estable: el emparejamiento image-major
    depende de el para ser reproducible."""
    labels = json.loads((ROOT / f"labels_{cls}.json").read_text())
    raw_vecs = json.loads((ROOT / f"label_vectors_{cls}.json").read_text())
    seq = []
    for word, freq in labels.items():
        if word not in raw_vecs:
            continue
        v_q = quantize_binary(np.array(raw_vecs[word], dtype=np.float32), M)
        seq.extend([v_q] * int(freq))
    return seq


def fill_agent(cls: str, encoder, g_min: np.ndarray, g_max: np.ndarray,
               latents: list = None):
    """Llena las tres memorias de un agente. Devuelve (mem_H, mem_L, mem_R)."""
    if latents is None:
        print(f"  Codificando {N_FILL} latentes de {cls}...")
        latents = get_instance_latents(encoder, cls, N_FILL)
    latents_q = [quantize_latent_global(z, g_min, g_max, Q) for z in latents]

    (MODELS_DIR / f"instance_latents_{cls}.json").write_text(
        json.dumps([z.tolist() for z in latents]))

    mem_H = HeteroAssociativeMemory(N, M, P, Q)
    mem_L = HomoAssociativeMemory(N, M)
    mem_R = HomoAssociativeMemory(P, Q)

    label_seq = build_label_sequence(cls)
    for v_q in label_seq:
        mem_L.register(v_q)

    L = len(label_seq)
    for i, z_q in enumerate(latents_q):
        mem_H.register(label_seq[i % L], z_q)
        mem_R.register(z_q)

    print(f"  {cls}: secuencia de {L} labels, "
          f"{len(latents_q)} instancias registradas")
    mem_H.print_stats(cls)
    mem_L.print_stats(f"{cls}_L")
    mem_R.print_stats(f"{cls}_R")
    return mem_H, mem_L, mem_R


def probe_recall(mem_H, cls: str, encoder, n_probes: int = 5):
    """Recall de prueba con los primeros labels de la clase."""
    from stage2_encoder import load_models
    _, decoder, _ = load_models()

    labels = json.loads((ROOT / f"labels_{cls}.json").read_text())
    raw_vecs = json.loads((ROOT / f"label_vectors_{cls}.json").read_text())
    stats = json.loads((MODELS_DIR / "latent_global_stats.json").read_text())
    g_min = np.array(stats["global_min"])
    g_max = np.array(stats["global_max"])

    sample_words = list(labels.keys())[:n_probes]
    print(f"  Probing {cls} con: {sample_words}")

    decoder.eval()
    results = []
    for word in sample_words:
        if word not in raw_vecs:
            continue
        v_q = quantize_binary(np.array(raw_vecs[word], dtype=np.float32), M)
        recalled_q, recognized, weight, *_ = mem_H.recall_from_left(v_q)
        if recognized:
            v_norm = recalled_q.astype(float) / (Q - 1)
            v_latent = (v_norm * (g_max - g_min) + g_min).astype(np.float32)
            z = torch.tensor(v_latent).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                img_recon = decoder(z)[0].cpu()
            results.append((word, True, weight, img_recon))
        else:
            results.append((word, False, 0.0, None))
    return results


def save_agent_memories(mem_H, mem_L, mem_R, cls: str):
    for suffix, mem in (("", mem_H), ("L_", mem_L), ("R_", mem_R)):
        path = MODELS_DIR / f"mem_dom_{suffix}{cls}.pkl"
        with open(path, "wb") as f:
            pickle.dump(mem, f)
        print(f"  Guardado -> {path.name}")


def load_agent_memories(cls: str):
    """Devuelve (mem_H, mem_L, mem_R); L y R pueden ser None si sus
    archivos no existen."""
    with open(MODELS_DIR / f"mem_dom_{cls}.pkl", "rb") as f:
        mem_H = pickle.load(f)
    mem_L = mem_R = None
    path_L = MODELS_DIR / f"mem_dom_L_{cls}.pkl"
    if path_L.exists():
        with open(path_L, "rb") as f:
            mem_L = pickle.load(f)
    path_R = MODELS_DIR / f"mem_dom_R_{cls}.pkl"
    if path_R.exists():
        with open(path_R, "rb") as f:
            mem_R = pickle.load(f)
    return mem_H, mem_L, mem_R


def visualize_probes(results: list, cls: str):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    good = [(w, img) for w, ok, wt, img in results if ok and img is not None]
    if not good:
        print(f"  Sin probes reconocidos para {cls}")
        return
    fig, axes = plt.subplots(1, len(good), figsize=(3 * len(good), 3))
    if len(good) == 1:
        axes = [axes]
    for ax, (word, img) in zip(axes, good):
        ax.imshow(img.permute(1, 2, 0).numpy().clip(0, 1))
        ax.set_title(word, fontsize=8)
        ax.axis("off")
    plt.suptitle(f"M_dom_H {cls} — probes de recall")
    plt.tight_layout()
    out = ROOT / f"stage5_probes_{cls}.png"
    plt.savefig(out, dpi=80)
    print(f"  Probes -> {out.name}")


def _encoder_mtime() -> float:
    """mtime del encoder (pesos o manifiesto). Si una memoria de contenido es
    más antigua, se llenó con OTRO encoder y está stale."""
    ts = 0.0
    for name in ("encoder.meta.json", "encoder.pt"):
        p = MODELS_DIR / name
        if p.exists():
            ts = max(ts, p.stat().st_mtime)
    return ts


def _is_stale(path) -> bool:
    """True si falta o si el encoder es más nuevo (memoria de un encoder viejo).
    Evita reutilizar silenciosamente un llenado hecho con otro espacio latente."""
    return (not path.exists()) or (path.stat().st_mtime < _encoder_mtime())


def _fill_inputs_mtime(cls: str) -> float:
    """mtime del insumo más nuevo del llenado de una clase: encoder + labels +
    vectores + escala de cuantización. Si una memoria es más vieja que cualquiera,
    se llenó con datos/representación distintos y está stale."""
    ts = _encoder_mtime()
    for p in (ROOT / f"labels_{cls}.json",
              ROOT / f"label_vectors_{cls}.json",
              MODELS_DIR / "label_quant_scale.json"):
        if p.exists():
            ts = max(ts, p.stat().st_mtime)
    return ts


def _is_stale_cls(path, cls: str) -> bool:
    """Como _is_stale pero también contra labels/vectores/escala de la clase:
    refill si cambió el vocabulario o la cuantización, no solo el encoder."""
    return (not path.exists()) or (path.stat().st_mtime < _fill_inputs_mtime(cls))


def run():
    encoder = load_encoder()

    stats_path = MODELS_DIR / "latent_global_stats.json"
    # Si el encoder cambió, las stats y las memorias guardadas pertenecen a
    # otro espacio latente. Se borran para forzar el recálculo.
    if stats_path.exists() and _is_stale(stats_path):
        stats_path.unlink()

    latents_by_cls = {}
    need_fill = any(
        _is_stale_cls(MODELS_DIR / f"mem_dom_{c}.pkl", c) for c in CLASSES)
    if need_fill or not stats_path.exists():
        for cls in CLASSES:
            print(f"  Codificando {N_FILL} latentes de {cls}...")
            latents_by_cls[cls] = get_instance_latents(encoder, cls, N_FILL)

    g_min, g_max = compute_global_latent_stats(encoder, latents_by_cls or None)
    agents_H = {}

    for cls in CLASSES:
        print(f"\n--- Llenando M_dom del agente {cls} ---")
        paths = [MODELS_DIR / f"mem_dom_{s}{cls}.pkl" for s in ("", "L_", "R_")]
        if all(p.exists() for p in paths) and not any(_is_stale_cls(p, cls) for p in paths):
            print("  Memorias existentes y vigentes, cargando.")
            mem_H, mem_L, mem_R = load_agent_memories(cls)
        else:
            mem_H, mem_L, mem_R = fill_agent(
                cls, encoder, g_min, g_max, latents=latents_by_cls.get(cls))
            save_agent_memories(mem_H, mem_L, mem_R, cls)

        agents_H[cls] = mem_H
        results = probe_recall(mem_H, cls, encoder)
        for word, ok, wt, _ in results:
            print(f"    '{word}': recognized={ok}, weight={wt:.2f}")
        visualize_probes(results, cls)

    print("\nEtapa 5 COMPLETADA.")
    return agents_H


if __name__ == "__main__":
    run()
