"""
Experimento 5 — Prototipo emergente: delta (promedio) vs instancias.

Ablación del PROTOCOLO DE LLENADO con ambos brazos reconstruidos EN MEMORIA
sobre las mismas 50 imágenes por clase y la misma masa de registros:

  DELTA       label×freq → el MISMO latente promediado (np.mean de las 50).
              La abstracción se hace FUERA de la memoria (protocolo v1).
  INSTANCIAS  label×freq → latente real (round-robin sobre las 50).
              La abstracción la acumula la propia relación (protocolo v2+).

Nota de vigencia (limpia jul 2026): la versión anterior usaba los pickles de
stage5 como brazo "viejo", lo cual quedó obsoleto cuando stage5 pasó a llenar
por instancias + augmentación: esa comparación medía cobertura (800 registros
vs 50), no la estrategia de llenado. Ahora ambos brazos son en-memoria y solo
difieren en DÓNDE ocurre la abstracción.

Hipótesis (las originales, sobre brazos comparables):
  H1. instancias → variedad genuina del recall (muestrea modos reales).
  H2. instancias → el reconocimiento inverso acepta imágenes individuales
      (la nube está contenida, no solo el centroide).
  H3. el routing temprano corregido no se degrada al cambiar el llenado.
  H4. la entropía de M_dom_H sube (distribución rica, fiel a Pineda).

M_dom_L compartido (el lado label no cambia entre brazos).
No modifica ningún artefacto previo. Salidas en results/exp5_entropic_prototype/

Uso:  python run_experiment5.py
"""
import csv
import io
import json
import sys
import contextlib
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = ROOT / "results" / "exp5_entropic_prototype"
OUT_DIR.mkdir(parents=True, exist_ok=True)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
from PIL import Image

from quantizer import quantize_binary
from hetero_memory import HeteroAssociativeMemory
from associative_memory import HomoAssociativeMemory
from stage5_fill import (
    load_agent_memories, load_encoder, compute_global_latent_stats,
    quantize_latent_global, IMG_TRANSFORM, DATA_DIR,
)
from stage6_interaction import (
    Agent, CLASSES, M_LABEL, N, P_LATENT, Q_LATENT,
    get_nlp, load_all_vectors, tokenize_query, prevectorize,
    get_fasttext_vector, token_in_vocabulary,
)

N_IMAGES   = 50     # mismas 50 que usó stage5 para el promedio
N_TEST     = 10     # imágenes held-out por clase para generalización
N_SAMPLES  = 12     # repeticiones de recall para medir variedad
GRID_SHOW  = 5      # muestras decodificadas en la figura
CUE_BY_CLS = {"apple": "fruit", "horse": "mane", "car": "vehicle",
              "cow": "milk", "cup": "drink", "dog": "pet",
              "pear": "pome", "tomato": "vegetable"}


# Construcción del llenado entrópico

def class_latents(encoder, cls, split, k):
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    paths = splits[cls][split][:k]
    zs = []
    encoder.eval()
    with torch.no_grad():
        for p in paths:
            img = Image.open(p).convert("RGB").resize((128, 128))
            t = IMG_TRANSFORM(img).unsqueeze(0)
            zs.append(encoder(t).cpu().numpy()[0])
    return zs


def build_entropic_agent(cls, latents_q, mem_L_shared):
    """label×freq → latente real (round-robin). Misma masa que stage5."""
    labels = json.loads((ROOT / f"labels_{cls}.json").read_text())
    raw    = json.loads((ROOT / f"label_vectors_{cls}.json").read_text())
    with contextlib.redirect_stdout(io.StringIO()):
        mem_H = HeteroAssociativeMemory(N, M_LABEL, P_LATENT, Q_LATENT)
        mem_R = HomoAssociativeMemory(P_LATENT, Q_LATENT)
    idx = 0
    n_reg = 0
    for word, freq in labels.items():
        if word not in raw:
            continue
        v_q = quantize_binary(np.array(raw[word], dtype=np.float32), M_LABEL)
        for _ in range(freq):
            z_q = latents_q[idx % len(latents_q)]
            with contextlib.redirect_stdout(io.StringIO()):
                mem_H.register(v_q, z_q)
            idx += 1
            n_reg += 1
    for z_q in latents_q:
        mem_R.register(z_q)
    print(f"    {cls}: {n_reg} registros hetero (round-robin sobre "
          f"{len(latents_q)} latentes reales)")
    return Agent(cls, mem_H, mem_dom_L=mem_L_shared, mem_dom_R=mem_R)


def build_delta_agent(cls, z_mean_q, n_latents, mem_L_shared):
    """Protocolo v1 reconstruido: label×freq → SIEMPRE el mismo latente
    promediado (la abstracción ocurre fuera de la memoria, que recibe una
    distribución degenerada — un delta). Misma masa de registros que el
    brazo de instancias: mem_H registra label_seq completo y mem_R recibe
    el delta n_latents veces."""
    labels = json.loads((ROOT / f"labels_{cls}.json").read_text())
    raw    = json.loads((ROOT / f"label_vectors_{cls}.json").read_text())
    with contextlib.redirect_stdout(io.StringIO()):
        mem_H = HeteroAssociativeMemory(N, M_LABEL, P_LATENT, Q_LATENT)
        mem_R = HomoAssociativeMemory(P_LATENT, Q_LATENT)
    n_reg = 0
    for word, freq in labels.items():
        if word not in raw:
            continue
        v_q = quantize_binary(np.array(raw[word], dtype=np.float32), M_LABEL)
        for _ in range(freq):
            with contextlib.redirect_stdout(io.StringIO()):
                mem_H.register(v_q, z_mean_q)
            n_reg += 1
    for _ in range(n_latents):
        mem_R.register(z_mean_q)
    print(f"    {cls}: {n_reg} registros hetero (todos al mismo latente "
          f"promediado)")
    return Agent(cls, mem_H, mem_dom_L=mem_L_shared, mem_dom_R=mem_R)


# Métricas

def recall_samples(agent, v_q, n):
    """n recalls del mismo cue. Devuelve lista de r_q (o None si rechazo)."""
    outs = []
    for _ in range(n):
        with contextlib.redirect_stdout(io.StringIO()):
            r_q, recognized, w, *_ = agent.mem_dom_H.recall_from_left(v_q)
        outs.append(r_q.copy() if recognized else None)
    return outs


def variety_stats(samples):
    ok = [s for s in samples if s is not None]
    if len(ok) < 2:
        return {"n_ok": len(ok), "distinct": len(ok), "mean_pair_l1": 0.0}
    arr = np.stack(ok)
    distinct = len({tuple(r) for r in arr})
    dists = [np.abs(arr[i] - arr[j]).mean()
             for i in range(len(arr)) for j in range(i + 1, len(arr))]
    return {"n_ok": len(ok), "distinct": distinct,
            "mean_pair_l1": float(np.mean(dists))}


def reverse_accept(agent, z_q):
    """Reconocimiento inverso unilateral: containment de la proyección dim=1."""
    mem_H = agent.mem_dom_H
    cb = mem_H.validate(z_q, 1)
    with contextlib.redirect_stdout(io.StringIO()):
        proj = mem_H.project(cb, np.ones(len(cb), dtype=float), 1)
    return np.count_nonzero(np.sum(proj, axis=1) == 0) == 0


def corrected_score(agent, v_q):
    """Scoring oficial: gate de containment (Agent.recognize_gated), sin
    división por mem.mean — con el llenado por instancias es redundante."""
    return agent.recognize_gated(v_q)


def early_accuracy(agents, nlp, vectors):
    from eval_bank import ALL_QUERIES, GROUND_TRUTH
    ok = rej = 0
    for query, truth in zip(ALL_QUERIES[:80], GROUND_TRUTH[:80]):
        # Sin filtro léxico: cada token con vector fastText real entra como
        # pista; el rechazo lo decide la EAM.
        scores = {cls: 0.0 for cls in CLASSES}
        represented = 0
        for tok in tokenize_query(query, nlp):
            v = get_fasttext_vector(tok, vectors, allow_fallback=False)
            if v is None:
                continue
            represented += 1
            v_q = quantize_binary(np.asarray(v, dtype=np.float32), M_LABEL)
            for cls in CLASSES:
                scores[cls] += corrected_score(agents[cls], v_q)
        if represented == 0 or sum(scores.values()) == 0:
            rej += 1
        elif max(scores, key=scores.get) == truth:
            ok += 1
    return ok / 80, rej / 80


def decode(decoder, r_q, g_min, g_max):
    v = r_q.astype(float) / (Q_LATENT - 1)
    z = (v * (g_max - g_min) + g_min).astype(np.float32)
    with torch.no_grad():
        img = decoder(torch.tensor(z).unsqueeze(0))[0].clamp(0, 1)
    return img.permute(1, 2, 0).numpy()


# Main

def main():
    print("=" * 64)
    print("  EXPERIMENTO 5 — prototipo emergente (llenado entrópico)")
    print("=" * 64)

    print("\nCargando encoder/decoder y stats globales...")
    encoder = load_encoder()
    from stage2_encoder import load_models
    _, decoder, _ = load_models()
    decoder.eval()
    g_min, g_max = compute_global_latent_stats(encoder)

    print("Cargando M_dom_L compartido (stage5, solo lectura)...")
    mem_Ls = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for cls in CLASSES:
            _, mem_L, _ = load_agent_memories(cls)
            mem_Ls[cls] = mem_L

    print("Construyendo ambos brazos EN MEMORIA (mismas 50 imágenes/clase, "
          "misma masa)...")
    delta_agents, inst_agents = {}, {}
    train_latents_q = {}
    for cls in CLASSES:
        zs = class_latents(encoder, cls, "train", N_IMAGES)
        zq = [quantize_latent_global(z, g_min, g_max, Q_LATENT) for z in zs]
        train_latents_q[cls] = zq
        z_mean_q = quantize_latent_global(
            np.mean(np.stack(zs), axis=0), g_min, g_max, Q_LATENT)
        delta_agents[cls] = build_delta_agent(
            cls, z_mean_q, len(zq), mem_Ls[cls])
        inst_agents[cls] = build_entropic_agent(cls, zq, mem_Ls[cls])

    ARMS = [("delta", delta_agents), ("inst", inst_agents)]
    metrics = {"delta": {}, "inst": {}}

    # H4: entropía de M_dom_H
    print("\n[H4] Entropía de M_dom_H (media del tensor):")
    with contextlib.redirect_stdout(io.StringIO()):
        for arm, ags in ARMS:
            metrics[arm]["entropy"] = {
                cls: float(ags[cls].mem_dom_H.entropy) for cls in CLASSES}
    for cls in CLASSES:
        print(f"  {cls:<6} delta={metrics['delta']['entropy'][cls]:.4f}   "
              f"inst={metrics['inst']['entropy'][cls]:.4f}")

    # H1: variedad del recall
    print(f"\n[H1] Variedad del recall ({N_SAMPLES} muestras por cue):")
    nlp = get_nlp()
    vectors = load_all_vectors(nlp)   # alias por lema: spaCy es parte del core
    from eval_bank import ALL_QUERIES
    _toks = set(CUE_BY_CLS.values())
    for _q in ALL_QUERIES:
        _toks.update(tokenize_query(_q, nlp))
    prevectorize(vectors, _toks, allow_fallback=False)
    grid_imgs = {"delta": {}, "inst": {}}
    for arm, ags in ARMS:
        metrics[arm]["variety"] = {}
        for cls in CLASSES:
            cue = CUE_BY_CLS[cls]
            v = np.array(get_fasttext_vector(cue, vectors), dtype=np.float32)
            v_q = quantize_binary(v, M_LABEL)
            samples = recall_samples(ags[cls], v_q, N_SAMPLES)
            st = variety_stats(samples)
            metrics[arm]["variety"][cls] = st
            ok = [s for s in samples if s is not None][:GRID_SHOW]
            grid_imgs[arm][cls] = [decode(decoder, r, g_min, g_max)
                                   for r in ok]
            print(f"  [{arm:>4}] {cls:<6} cue='{cue:<7}'  "
                  f"distintos={st['distinct']:2d}/{st['n_ok']:2d}  "
                  f"L1 medio entre pares={st['mean_pair_l1']:.3f}")

    # H2: aceptación inversa de imágenes reales
    print(f"\n[H2] Reconocimiento inverso (containment dim=1):")
    for arm, ags in ARMS:
        metrics[arm]["reverse"] = {}
        for cls in CLASSES:
            tr_acc = np.mean([reverse_accept(ags[cls], zq)
                              for zq in train_latents_q[cls][:20]])
            zs_te = class_latents(encoder, cls, "test", N_TEST)
            te_q = [quantize_latent_global(z, g_min, g_max, Q_LATENT)
                    for z in zs_te]
            te_acc = np.mean([reverse_accept(ags[cls], zq) for zq in te_q])
            metrics[arm]["reverse"][cls] = {
                "train": float(tr_acc), "test": float(te_acc)}
            print(f"  [{arm:>4}] {cls:<6} train={tr_acc*100:5.1f}%   "
                  f"test={te_acc*100:5.1f}%")

    # H3: routing temprano corregido intacto
    print("\n[H3] Routing temprano corregido (banco de 80):")
    for arm, ags in ARMS:
        acc, rej = early_accuracy(ags, nlp, vectors)
        metrics[arm]["early"] = {"acc": acc, "rej": rej}
        print(f"  [{arm:>4}] acc={acc*100:5.1f}%   rechazo={rej*100:4.1f}%")

    # Figura 1: grid de recalls decodificados
    rows = []
    for cls in CLASSES:
        rows.append(("delta · " + cls, grid_imgs["delta"][cls]))
        rows.append(("inst · " + cls, grid_imgs["inst"][cls]))
    fig, axes = plt.subplots(len(rows), GRID_SHOW,
                             figsize=(2.1 * GRID_SHOW, 2.15 * len(rows)))
    for r, (label, imgs) in enumerate(rows):
        for c in range(GRID_SHOW):
            ax = axes[r, c]
            if c < len(imgs):
                ax.imshow(np.clip(imgs[c], 0, 1))
            ax.set_xticks([]); ax.set_yticks([])
            if c == 0:
                ax.set_ylabel(label, fontsize=9)
    fig.suptitle("Recall ×5 del mismo cue — llenado delta (promedio) vs "
                 "instancias (round-robin)", fontsize=12)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig1_recall_variety_grid.png", dpi=140)
    plt.close(fig)

    # Figura 2: aceptación inversa
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    x = np.arange(len(CLASSES))
    for off, arm, color in [(-0.27, "delta", "#95a5a6"),
                            (0.07, "inst", "#1D9E75")]:
        tr = [metrics[arm]["reverse"][c]["train"] for c in CLASSES]
        te = [metrics[arm]["reverse"][c]["test"] for c in CLASSES]
        ax.bar(x + off, tr, 0.17, color=color, label=f"{arm} · train")
        ax.bar(x + off + 0.17, te, 0.17, color=color, alpha=0.55,
               label=f"{arm} · test")
    ax.set_xticks(x, CLASSES); ax.set_ylim(0, 1.05)
    ax.set_ylabel("tasa de aceptación (containment inverso)")
    ax.set_title("Reconocimiento de imágenes reales — centroide vs nube")
    ax.legend(fontsize=9); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig2_reverse_acceptance.png", dpi=150)
    plt.close(fig)

    # Persistencia de métricas + reporte
    (OUT_DIR / "metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8")

    rep = [
        "# Experimento 5 — prototipo emergente: delta vs instancias",
        "",
        "Ablación del protocolo de llenado con ambos brazos EN MEMORIA sobre",
        "las mismas 50 imágenes/clase y la misma masa de registros. DELTA:",
        "label×freq → el mismo latente promediado (abstracción fuera de la",
        "memoria, protocolo v1). INSTANCIAS: label×freq → latente real",
        "round-robin (la relación acumula la distribución, protocolo v2+).",
        "M_dom_L compartido; solo cambia el lado derecho de M_dom_H y M_dom_R.",
        "",
        "## Resultados",
        "",
        "| hipótesis | métrica | delta (promedio) | instancias |",
        "|---|---|---|---|",
    ]
    v_old = np.mean([metrics["delta"]["variety"][c]["distinct"]
                     for c in CLASSES])
    v_new = np.mean([metrics["inst"]["variety"][c]["distinct"]
                     for c in CLASSES])
    rep.append(f"| H1 variedad | recalls distintos /{N_SAMPLES} | "
               f"{v_old:.1f} | {v_new:.1f} |")
    for split in ("train", "test"):
        o = np.mean([metrics["delta"]["reverse"][c][split] for c in CLASSES])
        nw = np.mean([metrics["inst"]["reverse"][c][split] for c in CLASSES])
        rep.append(f"| H2 aceptación inversa ({split}) | media "
                   f"{len(CLASSES)} clases | {o:.1%} | {nw:.1%} |")
    rep.append(f"| H3 routing temprano | acc (rechazo) | "
               f"{metrics['delta']['early']['acc']:.1%} "
               f"({metrics['delta']['early']['rej']:.1%}) | "
               f"{metrics['inst']['early']['acc']:.1%} "
               f"({metrics['inst']['early']['rej']:.1%}) |")
    eo = np.mean(list(metrics["delta"]["entropy"].values()))
    en = np.mean(list(metrics["inst"]["entropy"].values()))
    rep.append(f"| H4 entropía M_dom_H | media {len(CLASSES)} clases | "
               f"{eo:.4f} | {en:.4f} |")
    rep += [
        "",
        "## Detalle variedad por clase",
        "",
        "| clase | cue | distintos delta | distintos inst | L1 delta | L1 inst |",
        "|---|---|---|---|---|---|",
    ]
    for cls in CLASSES:
        ov = metrics["delta"]["variety"][cls]
        nv = metrics["inst"]["variety"][cls]
        rep.append(f"| {cls} | {CUE_BY_CLS[cls]} | "
                   f"{ov['distinct']}/{ov['n_ok']} | "
                   f"{nv['distinct']}/{nv['n_ok']} | "
                   f"{ov['mean_pair_l1']:.3f} | {nv['mean_pair_l1']:.3f} |")
    rep += [
        "",
        "## Archivos",
        "- metrics.json · fig1_recall_variety_grid.png · "
        "fig2_reverse_acceptance.png",
        "",
        "Nota: ningún artefacto previo modificado; ambos brazos viven solo",
        "en memoria durante la corrida.",
    ]
    (OUT_DIR / "report.md").write_text("\n".join(rep), encoding="utf-8")
    print(f"\nSalidas -> {OUT_DIR}")
    print("EXPERIMENTO 5 COMPLETADO.")


if __name__ == "__main__":
    main()
