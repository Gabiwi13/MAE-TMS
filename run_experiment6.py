"""
Experimento 6 — Curva de capacidad del llenado por instancias.

Pregunta: ¿cuántas imágenes debe "comer" la memoria de dominio? ETH-80
ofrece 328 train por clase; el exp. 5 usó 50. Al escalar N:
  - ¿la generalización a imágenes nuevas (test) aparece sola por cobertura,
    sin necesidad de ξ>0?
  - ¿en qué punto la memoria se satura y empieza a aceptar imágenes de
    OTRAS clases (falsos aceptos — la promiscuidad, ahora en el latente)?
  - ¿el recall mantiene variedad sin volverse incoherente?
  - ¿el routing por labels (exp. 3) permanece estable?

Es la curva canónica de capacidad de Pineda (precisión vs llenado),
reproducida en nuestro dominio latente.

Protocolo de llenado (image-major): para cada imagen i de N se registra
(label_seq[i % L], z_i), donde label_seq expande los labels por frecuencia.
Registros por clase = N (las masas quedan igualadas entre clases por
construcción — se verifica que el routing no dependa de ello).

Brazos N ∈ {25, 50, 100, 200, 328}, procesados secuencialmente con
liberación de memoria (cada tensor HAM4D ≈ 86 MB).

Solo lectura de artefactos previos. Salidas en results/exp6_capacity/

Uso:  python run_experiment6.py
"""
import gc
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

OUT_DIR = ROOT / "results" / "exp6_capacity"
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

N_VALUES   = [25, 50, 100, 200, 328]
N_EVAL     = 20      # imágenes muestreadas por métrica de aceptación
N_SAMPLES  = 12      # recalls por cue para variedad
GRID_SHOW  = 5
CUE_BY_CLS = {"apple": "fruit", "horse": "mane", "car": "vehicle",
              "cow": "milk", "cup": "drink", "dog": "pet",
              "pear": "pome", "tomato": "vegetable"}
DOMAIN_COLOR = {"apple": "#e74c3c", "horse": "#2980b9", "car": "#27ae60",
                "cow": "#8e44ad", "cup": "#f39c12", "dog": "#16a085",
                "pear": "#7f8c8d", "tomato": "#c0392b"}


def class_latents_q(encoder, cls, split, k, g_min, g_max):
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    paths = splits[cls][split][:k]
    out = []
    encoder.eval()
    with torch.no_grad():
        for p in paths:
            img = Image.open(p).convert("RGB").resize((128, 128))
            z = encoder(IMG_TRANSFORM(img).unsqueeze(0)).cpu().numpy()[0]
            out.append(quantize_latent_global(z, g_min, g_max, Q_LATENT))
    return out


def label_sequence(cls, vectors_raw):
    labels = json.loads((ROOT / f"labels_{cls}.json").read_text())
    seq = []
    for word, freq in labels.items():
        if word not in vectors_raw:
            continue
        v_q = quantize_binary(np.array(vectors_raw[word], dtype=np.float32),
                              M_LABEL)
        seq.extend([v_q] * freq)
    return seq


def build_agent_n(cls, n_imgs, train_q, label_seq, mem_L_shared):
    with contextlib.redirect_stdout(io.StringIO()):
        mem_H = HeteroAssociativeMemory(N, M_LABEL, P_LATENT, Q_LATENT)
        mem_R = HomoAssociativeMemory(P_LATENT, Q_LATENT)
    L = len(label_seq)
    for i in range(n_imgs):
        with contextlib.redirect_stdout(io.StringIO()):
            mem_H.register(label_seq[i % L], train_q[i])
        mem_R.register(train_q[i])
    return Agent(cls, mem_H, mem_dom_L=mem_L_shared, mem_dom_R=mem_R)


def reverse_accept(agent, z_q):
    mem_H = agent.mem_dom_H
    cb = mem_H.validate(z_q, 1)
    with contextlib.redirect_stdout(io.StringIO()):
        proj = mem_H.project(cb, np.ones(len(cb), dtype=float), 1)
    return np.count_nonzero(np.sum(proj, axis=1) == 0) == 0


def corrected_score(agent, v_q, mem_mean):
    return agent.recognize_gated(v_q)


def early_accuracy(agents, mem_means, bank):
    ok = rej = 0
    for tokens_vq, truth in bank:
        if not tokens_vq:
            rej += 1
            continue
        scores = {cls: 0.0 for cls in CLASSES}
        for v_q in tokens_vq:
            for cls in CLASSES:
                scores[cls] += corrected_score(agents[cls], v_q,
                                               mem_means[cls])
        if sum(scores.values()) == 0:
            rej += 1
        elif max(scores, key=scores.get) == truth:
            ok += 1
    return ok / len(bank), rej / len(bank)


def recall_samples(agent, v_q, n):
    outs = []
    for _ in range(n):
        with contextlib.redirect_stdout(io.StringIO()):
            r_q, recognized, w, *_ = agent.mem_dom_H.recall_from_left(v_q)
        outs.append(r_q.copy() if recognized else None)
    return outs


def decode(decoder, r_q, g_min, g_max):
    v = r_q.astype(float) / (Q_LATENT - 1)
    z = (v * (g_max - g_min) + g_min).astype(np.float32)
    with torch.no_grad():
        img = decoder(torch.tensor(z).unsqueeze(0))[0].clamp(0, 1)
    return img.permute(1, 2, 0).numpy()


def main():
    print("=" * 64)
    print("  EXPERIMENTO 6 — curva de capacidad (N imágenes registradas)")
    print("=" * 64)

    print("\nPreparando encoder, decoder, stats, latentes y banco...")
    encoder = load_encoder()
    from stage2_encoder import load_models
    _, decoder, _ = load_models()
    decoder.eval()
    g_min, g_max = compute_global_latent_stats(encoder)

    train_q, test_q, label_seqs, mem_Ls = {}, {}, {}, {}
    with contextlib.redirect_stdout(io.StringIO()):
        for cls in CLASSES:
            _, mem_L, _ = load_agent_memories(cls)
            mem_Ls[cls] = mem_L
    nlp = get_nlp()
    vectors = load_all_vectors(nlp)   # alias por lema: spaCy es parte del core
    for cls in CLASSES:
        print(f"  codificando {cls} (328 train + 82 test)...")
        train_q[cls] = class_latents_q(encoder, cls, "train", 328,
                                       g_min, g_max)
        test_q[cls]  = class_latents_q(encoder, cls, "test", 82,
                                       g_min, g_max)
        raw = json.loads((ROOT / f"label_vectors_{cls}.json").read_text())
        label_seqs[cls] = label_sequence(cls, raw)

    from eval_bank import ALL_QUERIES, GROUND_TRUTH
    qg = list(zip(ALL_QUERIES[:80], GROUND_TRUTH[:80]))
    all_tokens = set()
    for query, _ in qg:
        all_tokens.update(tokenize_query(query, nlp))
    prevectorize(vectors, all_tokens, allow_fallback=False)
    bank = []
    for query, truth in qg:
        # Sin filtro léxico: cada token con vector fastText real entra como
        # pista; los no representables se descartan y la EAM decide el resto.
        vqs = []
        for t in tokenize_query(query, nlp):
            v = get_fasttext_vector(t, vectors, allow_fallback=False)
            if v is not None:
                vqs.append(quantize_binary(np.asarray(v, dtype=np.float32), M_LABEL))
        bank.append((vqs, truth))

    rng = np.random.RandomState(7)
    results = []
    apple_strips = {}

    for n_imgs in N_VALUES:
        print(f"\n--- N = {n_imgs} imágenes por clase ---")
        agents = {}
        for cls in CLASSES:
            agents[cls] = build_agent_n(cls, n_imgs, train_q[cls],
                                        label_seqs[cls], mem_Ls[cls])
        mem_means = {}
        with contextlib.redirect_stdout(io.StringIO()):
            for cls in CLASSES:
                mem_means[cls] = float(agents[cls].mem_dom_H.mean)
            entropies = {cls: float(agents[cls].mem_dom_H.entropy)
                         for cls in CLASSES}

        row = {"N": n_imgs}
        # aceptación: train propio / test propio / cruzada (falsos)
        own_tr, own_te, cross = [], [], []
        for cls in CLASSES:
            tr_idx = rng.choice(n_imgs, size=min(N_EVAL, n_imgs),
                                replace=False)
            own_tr += [reverse_accept(agents[cls], train_q[cls][i])
                       for i in tr_idx]
            te_idx = rng.choice(82, size=N_EVAL, replace=False)
            own_te += [reverse_accept(agents[cls], test_q[cls][i])
                       for i in te_idx]
            for other in CLASSES:
                if other == cls:
                    continue
                ot_idx = rng.choice(82, size=N_EVAL // 2, replace=False)
                cross += [reverse_accept(agents[cls], test_q[other][i])
                          for i in ot_idx]
        row["own_train"] = float(np.mean(own_tr))
        row["own_test"]  = float(np.mean(own_te))
        row["cross_false"] = float(np.mean(cross))

        # variedad del recall + strip de manzanas
        var_d, var_l1 = [], []
        for cls in CLASSES:
            v = np.array(get_fasttext_vector(CUE_BY_CLS[cls], vectors),
                         dtype=np.float32)
            v_q = quantize_binary(v, M_LABEL)
            samples = recall_samples(agents[cls], v_q, N_SAMPLES)
            ok = [s for s in samples if s is not None]
            if cls == "apple":
                apple_strips[n_imgs] = [decode(decoder, r, g_min, g_max)
                                        for r in ok[:GRID_SHOW]]
            if len(ok) >= 2:
                arr = np.stack(ok)
                var_d.append(len({tuple(r) for r in arr}) / len(ok))
                var_l1.append(np.mean([np.abs(arr[i] - arr[j]).mean()
                                       for i in range(len(arr))
                                       for j in range(i + 1, len(arr))]))
        row["variety_frac"] = float(np.mean(var_d)) if var_d else 0.0
        row["variety_l1"]   = float(np.mean(var_l1)) if var_l1 else 0.0

        # routing + entropía
        acc, rej = early_accuracy(agents, mem_means, bank)
        row["routing_acc"], row["routing_rej"] = acc, rej
        row["entropy_mean"] = float(np.mean(list(entropies.values())))
        results.append(row)
        print(f"  own_train={row['own_train']*100:5.1f}%  "
              f"own_test={row['own_test']*100:5.1f}%  "
              f"cross_false={row['cross_false']*100:5.1f}%")
        print(f"  variedad={row['variety_frac']*100:4.0f}%  "
              f"L1={row['variety_l1']:.2f}  routing={acc*100:5.1f}%  "
              f"H={row['entropy_mean']:.3f}")

        del agents
        gc.collect()

    # CSV
    import csv as _csv
    with open(OUT_DIR / "results_capacity.csv", "w", newline="",
              encoding="utf-8") as f:
        w = _csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader(); w.writerows(results)

    Ns = [r["N"] for r in results]

    # fig1: curva de operación (generalización vs falsos)
    fig, ax = plt.subplots(figsize=(9.2, 5.4))
    ax.plot(Ns, [r["own_train"] for r in results], "o-", color="#534AB7",
            lw=2.2, label="train propio (memorización)")
    ax.plot(Ns, [r["own_test"] for r in results], "s-", color="#1D9E75",
            lw=2.2, label="test propio (generalización)")
    ax.plot(Ns, [r["cross_false"] for r in results], "^--", color="#e74c3c",
            lw=2.2, label="otras clases (falsos aceptos)")
    ax.set_xlabel("N imágenes registradas por clase")
    ax.set_ylabel("tasa de aceptación (containment inverso, ξ=0)")
    ax.set_title("Curva de capacidad — cobertura vs saturación del latente")
    ax.set_ylim(-0.03, 1.05); ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig1_capacity_curve.png", dpi=150)
    plt.close(fig)

    # fig2: variedad + routing + entropía vs N
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2))
    axes[0].plot(Ns, [r["variety_l1"] for r in results], "o-",
                 color="#1D9E75", lw=2)
    axes[0].set_title("variedad del recall (L1 medio)")
    axes[1].plot(Ns, [r["routing_acc"] for r in results], "o-",
                 color="#534AB7", lw=2)
    axes[1].axhline(0.975, ls=":", c="gray", lw=1)
    axes[1].set_ylim(0.8, 1.02); axes[1].set_title("routing temprano (acc)")
    axes[2].plot(Ns, [r["entropy_mean"] for r in results], "o-",
                 color="#e67e22", lw=2)
    axes[2].set_title("entropía media M_dom_H")
    for ax in axes:
        ax.set_xlabel("N imágenes")
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig2_variety_routing_entropy.png", dpi=150)
    plt.close(fig)

    # fig3: strip de manzanas por N
    fig, axes = plt.subplots(len(N_VALUES), GRID_SHOW,
                             figsize=(2.0 * GRID_SHOW, 2.05 * len(N_VALUES)))
    for r_i, n_imgs in enumerate(N_VALUES):
        imgs = apple_strips.get(n_imgs, [])
        for c in range(GRID_SHOW):
            ax = axes[r_i, c]
            if c < len(imgs):
                ax.imshow(np.clip(imgs[c], 0, 1))
            ax.set_xticks([]); ax.set_yticks([])
            if c == 0:
                ax.set_ylabel(f"N={n_imgs}", fontsize=10)
    fig.suptitle("Recall ×5 de 'fruit' (agente apple) según N registradas",
                 fontsize=12)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "fig3_apple_strips.png", dpi=140)
    plt.close(fig)

    # reporte
    rep = [
        "# Experimento 6 — curva de capacidad del llenado por instancias",
        "",
        "| N | train propio | test propio | falsos (otras clases) | "
        "variedad L1 | routing | entropía |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in results:
        rep.append(
            f"| {r['N']} | {r['own_train']:.0%} | {r['own_test']:.0%} | "
            f"{r['cross_false']:.0%} | {r['variety_l1']:.2f} | "
            f"{r['routing_acc']:.1%} | {r['entropy_mean']:.3f} |")
    rep += [
        "",
        "Protocolo image-major: registros por clase = N (masas igualadas).",
        "Aceptación = containment inverso unilateral con ξ=0.",
        "",
        "## Archivos",
        "- results_capacity.csv · fig1_capacity_curve.png",
        "- fig2_variety_routing_entropy.png · fig3_apple_strips.png",
    ]
    (OUT_DIR / "report.md").write_text("\n".join(rep), encoding="utf-8")
    print(f"\nSalidas -> {OUT_DIR}")
    print("EXPERIMENTO 6 COMPLETADO.")


if __name__ == "__main__":
    main()
