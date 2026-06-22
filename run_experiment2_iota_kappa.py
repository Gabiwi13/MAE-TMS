"""
Experimento 2 — ¿Las defensas nativas de Pineda (iota, kappa) eliminan el
sesgo de densidad que B1 tuvo que corregir?

Hipótesis
---------
El sesgo de apple (exp. 1) aparece con iota=kappa=0, es decir, con las dos
defensas del framework apagadas:
  - iota poda las celdas de la relación con peso < iota·(suma/count) por par
    de features → des-satura la relación promiscua de apple (eslabón 2).
  - kappa exige reconocimiento relativo a la media de la propia memoria:
    reconocido ⇔ kappa·mean ≤ peso → neutraliza la ventaja de masa (eslabón 3).
Si la hipótesis es cierta, existe (iota, kappa) > 0 que iguala o supera la
accuracy de la normalización ÷mem.mean SIN salirse de la teoría — y entonces
B1 es la versión "a nivel sistema" de una defensa que el framework ya traía.

Diseño
------
Grid iota × kappa sobre el routing de fase temprana (banco de 80 queries del
ablation, ground truth conocido):
  score(agente) = activación media de project(v_q, pesos_L, dim=0)
                  gateada por:  (a) containment-iota: ninguna fila vacía
                                (b) kappa-gate: act_media ≥ kappa·mem.mean
Brazos por condición: GATED (solo defensas nativas) y GATED+NORM (÷mem.mean
encima, para medir complementariedad).

Downstream: para condiciones seleccionadas, se entrena M_dir con los winners
de la fase temprana y se mide accuracy madura RAW vs B1 → ¿sigue haciendo
falta B1 si el upstream está corregido?

Solo lectura de los pickles de stage5; las mutaciones de iota/kappa son
en-memoria (setters originales de Pineda). No se modifica ningún archivo
del experimento 1.

Uso:  python run_experiment2_iota_kappa.py
Salidas en results/exp2_iota_kappa/
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

# Consola Windows cp1252 no imprime ι/κ — forzar utf-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = ROOT / "results" / "exp2_iota_kappa"
OUT_DIR.mkdir(parents=True, exist_ok=True)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from quantizer import quantize_binary
from associative_memory import DirectoryMemory
from stage5_fill import load_agent_memories
from stage6_interaction import (
    CLASSES, AGENT_LIST, M_LABEL, N,
    get_nlp, load_all_vectors, tokenize_query,
    get_fasttext_vector, token_in_vocabulary,
)

# Grid del barrido
IOTAS  = [0.0, 0.25, 0.5, 1.0]
KAPPAS = [0.0, 0.5, 1.0, 1.5]

# Cues diagnósticos del exp. 1 (token, dominio esperado)
DIAG_CUES = [
    ("vehicle", "car"), ("automobile", "car"), ("engine", "car"),
    ("wheels", "car"),
    ("fruit", "apple"), ("red", "apple"), ("tree", "apple"),
    ("animal", "horse"), ("mane", "horse"), ("equine", "horse"),
    ("saddle", "horse"),
]


# Núcleo de scoring (defensas nativas)

def agent_score(mem_L, mem_H, v_q, kappa, normalize=False):
    """
    Score de routing de un agente con las defensas nativas activas.

    - iota actúa automáticamente: project() lee _full_iota_relation,
      que el setter de iota invalida y update() recalcula con la poda
      threshold = iota·(suma/count) por par de features (código original).
    - containment unilateral: si la proyección tiene alguna fila vacía,
      el cue no está contenido → score 0 (mismo criterio que recall()).
    - kappa-gate: adaptación unilateral del criterio original
      `recognized and (kappa·mean <= peso)` (hetero_associative_4d.py:240);
      con un solo cue usamos la activación media vs kappa·mem.mean.

    normalize=True añade ÷mem.mean encima (brazo GATED+NORM).
    """
    l_w = mem_L.recog_weights(v_q)
    mx = l_w.max()
    weights = (l_w / mx) if mx > 0 else np.ones(len(v_q), dtype=float)

    ca = mem_H.validate(v_q, 0)
    with contextlib.redirect_stdout(io.StringIO()):
        proj = mem_H.project(ca, weights, 0)          # iota ya aplicada
        mem_mean = float(mem_H.mean)

    # (a) containment-iota: ninguna fila del dominio derecho vacía
    if np.count_nonzero(np.sum(proj, axis=1) == 0) > 0:
        return 0.0

    total = float(np.sum(proj))
    count = int(np.count_nonzero(proj))
    if count == 0:
        return 0.0
    mean_act = total / count

    # (b) kappa-gate relativo a la media de la propia memoria
    if mem_mean > 0 and mean_act < kappa * mem_mean:
        return 0.0

    if normalize and mem_mean > 0:
        return mean_act / mem_mean
    return mean_act


def set_params(agents_mem, iota, kappa):
    """Mutación en-memoria vía setters originales (sin tocar pickles)."""
    for cls in CLASSES:
        mem_L, mem_H = agents_mem[cls]
        mem_L._am.iota  = iota
        mem_L._am.kappa = kappa
        mem_H.iota  = iota
        mem_H.kappa = kappa


# Evaluaciones

def route_query(query, agents_mem, kappa, nlp, vectors, tok_cache,
                normalize=False):
    """Routing de fase temprana. Devuelve (winner|None, tokens_usados)."""
    tokens = [t for t in tokenize_query(query, nlp)
              if token_in_vocabulary(t, vectors)]
    if not tokens:
        return None, []
    scores = {cls: 0.0 for cls in CLASSES}
    for tok in tokens:
        if tok not in tok_cache:
            v = np.array(get_fasttext_vector(tok, vectors), dtype=np.float32)
            tok_cache[tok] = quantize_binary(v, M_LABEL)
        v_q = tok_cache[tok]
        for cls in CLASSES:
            mem_L, mem_H = agents_mem[cls]
            scores[cls] += agent_score(mem_L, mem_H, v_q, kappa,
                                       normalize=normalize)
    if sum(scores.values()) == 0:
        return None, tokens
    return max(scores, key=scores.get), tokens


def eval_early(agents_mem, kappa, queries, gt, nlp, vectors, tok_cache,
               normalize=False, collect_mdir=None):
    """Accuracy temprana sobre el banco. Opcionalmente llena un M_dir."""
    ok = rej = 0
    for query, truth in zip(queries, gt):
        winner, tokens = route_query(query, agents_mem, kappa, nlp,
                                     vectors, tok_cache, normalize=normalize)
        if winner is None:
            rej += 1
            continue
        if winner == truth:
            ok += 1
        if collect_mdir is not None:
            widx = AGENT_LIST.index(winner)
            for tok in tokens:
                collect_mdir.register(tok_cache[tok], widx)
    n = len(queries)
    return ok / n, rej / n


def eval_diag(agents_mem, kappa, vectors, tok_cache, normalize=False):
    """Accuracy sobre los 11 cues diagnósticos (rechazo cuenta como fallo)."""
    ok = 0
    for tok, truth in DIAG_CUES:
        if not token_in_vocabulary(tok, vectors):
            continue
        if tok not in tok_cache:
            v = np.array(get_fasttext_vector(tok, vectors), dtype=np.float32)
            tok_cache[tok] = quantize_binary(v, M_LABEL)
        v_q = tok_cache[tok]
        scores = {}
        for cls in CLASSES:
            mem_L, mem_H = agents_mem[cls]
            scores[cls] = agent_score(mem_L, mem_H, v_q, kappa,
                                      normalize=normalize)
        if sum(scores.values()) > 0 and max(scores, key=scores.get) == truth:
            ok += 1
    return ok / len(DIAG_CUES)


def eval_mature(mdir, queries, gt, nlp, vectors, tok_cache, b1):
    """Accuracy madura: routing solo por M_dir (raw o B1)."""
    ok = rej = 0
    for query, truth in zip(queries, gt):
        tokens = [t for t in tokenize_query(query, nlp)
                  if token_in_vocabulary(t, vectors)]
        if not tokens:
            rej += 1
            continue
        agg = np.zeros(len(CLASSES), dtype=float)
        for tok in tokens:
            v_q = tok_cache[tok]
            agg += (mdir.predict_normalized(v_q, mode="linear")
                    if b1 else mdir.predict(v_q))
        if agg.sum() == 0:
            rej += 1
            continue
        if CLASSES[int(np.argmax(agg))] == truth:
            ok += 1
    n = len(queries)
    return ok / n, rej / n


# Main

def main():
    print("=" * 64)
    print("  EXPERIMENTO 2 — barrido iota × kappa (defensas nativas)")
    print("=" * 64)

    print("\nCargando memorias de stage5 (solo lectura)...")
    agents_mem = {}
    for cls in CLASSES:
        mem_H, mem_L, mem_R = load_agent_memories(cls)
        agents_mem[cls] = (mem_L, mem_H)

    nlp     = get_nlp()
    vectors = load_all_vectors(nlp)   # alias por lema: spaCy es parte del core
    from eval_bank import ALL_QUERIES, GROUND_TRUTH
    queries, gt = ALL_QUERIES[:80], GROUND_TRUTH[:80]
    tok_cache = {}

    rows = []
    n_cond = len(IOTAS) * len(KAPPAS)
    k_i = 0
    for iota in IOTAS:
        for kappa in KAPPAS:
            k_i += 1
            set_params(agents_mem, iota, kappa)
            # fuerza el recálculo de iota_relation una sola vez por condición
            with contextlib.redirect_stdout(io.StringIO()):
                for cls in CLASSES:
                    _ = agents_mem[cls][1]._full_iota_relation
                    _ = agents_mem[cls][1].mean

            acc_g,  rej_g  = eval_early(agents_mem, kappa, queries, gt,
                                        nlp, vectors, tok_cache)
            acc_gn, rej_gn = eval_early(agents_mem, kappa, queries, gt,
                                        nlp, vectors, tok_cache,
                                        normalize=True)
            diag_g  = eval_diag(agents_mem, kappa, vectors, tok_cache)
            diag_gn = eval_diag(agents_mem, kappa, vectors, tok_cache,
                                normalize=True)
            rows.append({
                "iota": iota, "kappa": kappa,
                "early_acc_gated":  round(acc_g, 4),
                "early_rej_gated":  round(rej_g, 4),
                "early_acc_norm":   round(acc_gn, 4),
                "early_rej_norm":   round(rej_gn, 4),
                "diag_acc_gated":   round(diag_g, 4),
                "diag_acc_norm":    round(diag_gn, 4),
            })
            print(f"  [{k_i:2d}/{n_cond}] ι={iota:<5} κ={kappa:<4} | "
                  f"early GATED={acc_g*100:5.1f}% (rej {rej_g*100:4.1f}%)  "
                  f"+NORM={acc_gn*100:5.1f}%  | diag {diag_g*100:5.1f}% / "
                  f"{diag_gn*100:5.1f}%")

    # CSV
    csv_path = OUT_DIR / "results_grid.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"\nCSV -> {csv_path}")

    # Heatmaps
    def heat(metric, title, fname, fmt="{:.0%}"):
        M = np.zeros((len(IOTAS), len(KAPPAS)))
        for r in rows:
            i = IOTAS.index(r["iota"]); j = KAPPAS.index(r["kappa"])
            M[i, j] = r[metric]
        fig, ax = plt.subplots(figsize=(7.2, 5.4))
        im = ax.imshow(M, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
        ax.set_xticks(range(len(KAPPAS)), [f"κ={k}" for k in KAPPAS])
        ax.set_yticks(range(len(IOTAS)),  [f"ι={i}" for i in IOTAS])
        for i in range(len(IOTAS)):
            for j in range(len(KAPPAS)):
                ax.text(j, i, fmt.format(M[i, j]), ha="center", va="center",
                        fontsize=11,
                        color="black" if 0.25 < M[i, j] < 0.85 else "white")
        ax.set_title(title)
        fig.colorbar(im, ax=ax, shrink=0.85)
        fig.tight_layout()
        fig.savefig(OUT_DIR / fname, dpi=150)
        plt.close(fig)
        print(f"  fig -> {fname}")

    heat("early_acc_gated",
         "Exp. 2 — accuracy temprana (defensas nativas ι/κ, sin normalizar)",
         "heatmap_early_acc_gated.png")
    heat("early_rej_gated",
         "Exp. 2 — tasa de rechazo (defensas nativas ι/κ)",
         "heatmap_early_rejection.png")
    heat("early_acc_norm",
         "Exp. 2 — accuracy temprana (ι/κ + ÷mem.mean)",
         "heatmap_early_acc_norm.png")
    heat("diag_acc_gated",
         "Exp. 2 — accuracy en 11 cues diagnósticos (ι/κ)",
         "heatmap_diag_gated.png")

    # Downstream: ¿sigue haciendo falta B1?
    print("\nDownstream — M_dir entrenado con el routing de cada condición:")
    best = max(rows, key=lambda r: (r["early_acc_gated"], -r["early_rej_gated"]))
    selected = [
        ("baseline ι=0 κ=0 (exp. 1)",      0.0,            0.0,            False),
        (f"mejor nativa ι={best['iota']} κ={best['kappa']}",
                                            best["iota"],   best["kappa"],  False),
        ("÷mem.mean con ι=0 κ=0",           0.0,            0.0,            True),
    ]
    down_rows = []
    for name, iota, kappa, normalize in selected:
        set_params(agents_mem, iota, kappa)
        with contextlib.redirect_stdout(io.StringIO()):
            for cls in CLASSES:
                _ = agents_mem[cls][1]._full_iota_relation
                _ = agents_mem[cls][1].mean
        mdir = DirectoryMemory(N, M_LABEL, len(CLASSES))
        e_acc, e_rej = eval_early(agents_mem, kappa, queries, gt, nlp,
                                  vectors, tok_cache, normalize=normalize,
                                  collect_mdir=mdir)
        m_raw, mr_rej = eval_mature(mdir, queries, gt, nlp, vectors,
                                    tok_cache, b1=False)
        m_b1,  mb_rej = eval_mature(mdir, queries, gt, nlp, vectors,
                                    tok_cache, b1=True)
        down_rows.append({
            "condicion": name, "iota": iota, "kappa": kappa,
            "norm_upstream": normalize,
            "early_acc": round(e_acc, 4), "early_rej": round(e_rej, 4),
            "mature_acc_raw": round(m_raw, 4),
            "mature_acc_b1":  round(m_b1, 4),
            "mdir_counts": str(mdir.agent_counts.tolist()),
        })
        print(f"  {name:<34} early={e_acc*100:5.1f}%  "
              f"mature RAW={m_raw*100:5.1f}%  B1={m_b1*100:5.1f}%  "
              f"counts={mdir.agent_counts.tolist()}")

    down_path = OUT_DIR / "results_downstream.csv"
    with open(down_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(down_rows[0].keys()))
        w.writeheader(); w.writerows(down_rows)
    print(f"CSV -> {down_path}")

    # Reporte
    base = next(r for r in rows if r["iota"] == 0 and r["kappa"] == 0)
    norm_ref = base["early_acc_norm"]
    lines = [
        "# Experimento 2 — iota y kappa como defensas contra el sesgo de densidad",
        "",
        "## Hipótesis",
        "Las defensas nativas del framework (ι: poda de la relación; κ: umbral",
        "relativo a la media de cada memoria) eliminan el sesgo de masa que en el",
        "experimento 1 obligó a introducir la normalización B1 / ÷mem.mean.",
        "",
        "## Setup",
        f"- Grid: ι ∈ {IOTAS} × κ ∈ {KAPPAS} (mutación en-memoria, setters originales)",
        "- Banco: 80 queries del ablation con ground truth (27/27/26)",
        "- Score: activación media de project() con pesos de M_dom_L,",
        "  gateada por containment-ι y por κ·mem.mean (adaptación unilateral",
        "  del criterio original de recognize()).",
        "",
        "## Resultados clave",
        f"- Baseline ι=0 κ=0 (exp. 1): early {base['early_acc_gated']:.1%}, "
        f"diag {base['diag_acc_gated']:.1%}",
        f"- Referencia ÷mem.mean (ι=0 κ=0): early {norm_ref:.1%}",
        f"- Mejor condición nativa: ι={best['iota']} κ={best['kappa']} → "
        f"early {best['early_acc_gated']:.1%} "
        f"(rechazo {best['early_rej_gated']:.1%}), "
        f"diag {best['diag_acc_gated']:.1%}",
        "",
        "## Tabla del grid (brazo GATED, sin normalizar)",
        "",
        "| ι \\ κ | " + " | ".join(str(k) for k in KAPPAS) + " |",
        "|---" * (len(KAPPAS) + 1) + "|",
    ]
    for iota in IOTAS:
        cells = []
        for kappa in KAPPAS:
            r = next(x for x in rows if x["iota"] == iota and x["kappa"] == kappa)
            cells.append(f"{r['early_acc_gated']:.0%} (rej {r['early_rej_gated']:.0%})")
        lines.append(f"| **{iota}** | " + " | ".join(cells) + " |")
    lines += [
        "",
        "## Downstream (¿sigue haciendo falta B1?)",
        "",
        "| condición | early | mature RAW | mature B1 | counts M_dir |",
        "|---|---|---|---|---|",
    ]
    for d in down_rows:
        lines.append(
            f"| {d['condicion']} | {d['early_acc']:.1%} | "
            f"{d['mature_acc_raw']:.1%} | {d['mature_acc_b1']:.1%} | "
            f"{d['mdir_counts']} |")
    lines += [
        "",
        "## Archivos",
        "- results_grid.csv · results_downstream.csv",
        "- heatmap_early_acc_gated.png · heatmap_early_rejection.png",
        "- heatmap_early_acc_norm.png · heatmap_diag_gated.png",
    ]
    (OUT_DIR / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Reporte -> {OUT_DIR / 'report.md'}")
    print("\nEXPERIMENTO 2 COMPLETADO.")


if __name__ == "__main__":
    main()
