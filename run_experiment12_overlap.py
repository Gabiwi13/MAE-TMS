"""
Experimento 12 — ¿La ventaja de partir crece con el solapamiento entre dominios?

Para cada par de clases se llena una EHAM única con las dos (M2, mismo llenado
que exp11 en N=200) y se responde con ella a las consultas reservadas de esas
dos clases. La referencia es el especialista (T-oráculo), cuyas respuestas a
las mismas consultas y semillas están en results/experimento11/raw.

Solapamiento por par, medido donde actúa el mecanismo: fracción de
coordenadas cuyos soportes (valores registrados) coinciden entre las dos
clases, en el lado de las etiquetas (300×16, homo L) y en el latente (64×32,
homo R); y número de etiquetas compartidas.

Predicción pre-registrada: la brecha de fidelidad de M2 respecto del
especialista (d_nn M2 − d_nn oráculo) crece con el solapamiento (Spearman
ρ > 0, p < 0.05 sobre 28 pares); con pares disjuntos la brecha es cercana a
cero.

Uso:  python run_experiment12_overlap.py [--seeds 42-46] [--reps 3] [--workers 12]
          [--pairs apple-tomato,car-cup] [--report-only]
"""
import argparse
import contextlib
import io
import itertools
import json
import os
import random
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from stage6_interaction import CLASSES, AGENT_LIST, N, M_LABEL, P_LATENT, Q_LATENT, Agent, get_nlp, load_all_vectors
from stage7_bidirectional import load_global_stats
from hetero_memory import HeteroAssociativeMemory
from associative_memory import HomoAssociativeMemory
from run_experiment9_member_loss import Judge, load_classifier, load_bank, recall_lived, live_levels_lived
from run_experiment11_monolithic import (
    load_pool, split_bank, shared_labels, N_TEXT_TRAIN_PER_CLASS, VARIANTS, load_cache, parse_seeds,
)

OUT_DIR = Path(os.environ.get("EXP12_OUT", ROOT / "results" / "experimento12"))
RAW_DIR = OUT_DIR / "raw"
EXP11_RAW = ROOT / "results" / "experimento11" / "raw"
N_IMG = 200
SEEDS = (42, 43, 44, 45, 46)
REPS = 3
PAIRS = list(itertools.combinations(CLASSES, 2))


# ---------- solapamiento ----------

def supports_from_cache():
    """Soportes (valor registrado o no) por coordenada de las homo de cada
    clase, desde el caché de N=200 de exp11."""
    cached = load_cache(N_IMG)
    sup = {}
    for cls, ag in cached["specialists"].items():
        sup[cls] = {"L": ag.mem_dom_L._am.relation > 0, "R": ag.mem_dom_R._am.relation > 0}
    del cached
    return sup


def overlap(sup_a, sup_b):
    """Jaccard medio por coordenada de los soportes de dos clases."""
    inter = (sup_a & sup_b).sum(axis=1)
    union = (sup_a | sup_b).sum(axis=1)
    return float(np.mean(inter / np.maximum(union, 1)))


def pair_overlaps(sup, shared):
    out = {}
    for a, b in PAIRS:
        vocab = {c: set(json.loads((ROOT / f"label_vectors_{c}.json").read_text())) for c in (a, b)}
        out[f"{a}-{b}"] = {"izquierda": overlap(sup[a]["L"], sup[b]["L"]),
                           "latente": overlap(sup[a]["R"], sup[b]["R"]),
                           "etiquetas_compartidas": sorted(vocab[a] & vocab[b])}
    return out


# ---------- memoria del par ----------

def build_pair(pool, seqs, pair):
    with contextlib.redirect_stdout(io.StringIO()):
        mem_H = HeteroAssociativeMemory(N, M_LABEL, P_LATENT, Q_LATENT)
        mem_L = HomoAssociativeMemory(N, M_LABEL)
        mem_R = HomoAssociativeMemory(P_LATENT, Q_LATENT)
    for cls in pair:
        for v_q in seqs[cls]:
            mem_L.register(v_q)
    with contextlib.redirect_stdout(io.StringIO()):
        for i in range(VARIANTS * N_IMG):
            for cls in pair:
                mem_H.register(seqs[cls][i % len(seqs[cls])], pool[cls][i])
                mem_R.register(pool[cls][i])
    return Agent("-".join(pair), mem_H, mem_dom_L=mem_L, mem_dom_R=mem_R)


CTX = {}


def init_worker(bank, held_idx, shared, sup_R):
    CTX.update(bank=bank, held_idx=held_idx, shared=shared, sup_R=sup_R)
    CTX["pool"], CTX["seqs"] = load_pool()
    g_min, g_max = load_global_stats()
    CTX["judge"] = Judge(load_classifier(), g_min, g_max)


def run_pair(args):
    pair, seeds, reps = args
    tag = "-".join(pair)
    out = RAW_DIR / f"{tag}.json"
    if out.exists():
        return str(out)
    t0 = time.time()
    bank, held_idx, shared, sup_R, judge = (CTX[k] for k in ("bank", "held_idx", "shared", "sup_R", "judge"))
    mono = build_pair(CTX["pool"], CTX["seqs"], pair)
    t_build = time.time() - t0
    rows = []
    for seed in seeds:
        random.seed(seed * 100)
        np.random.seed(seed * 100)
        for idx in held_idx:
            it = bank[idx]
            if it["truth"] not in pair:
                continue
            for r in range(reps):
                row = {"par": tag, "semilla": seed, "query": it["query"], "truth": it["truth"], "rep": r,
                       "responde": False}
                z_q, tok = recall_lived(mono, it["cues"])
                if z_q is not None:
                    j = judge.judge(z_q, it["tidx"])
                    comp = {c: float(np.mean(sup_R[c][np.arange(P_LATENT), z_q])) for c in pair}
                    other = [c for c in pair if c != it["truth"]][0]
                    row.update({"responde": True, "pista": tok, "pista_compartida": tok in shared,
                                "nn_ok": j["nn_cls"] == it["tidx"], "nn_cls": CLASSES[j["nn_cls"]],
                                "clf_ok": j["clf"] == it["tidx"], "d_nn_truth": j["d_nn_target"],
                                "compat_truth": comp[it["truth"]], "compat_otro": comp[other]})
                    if r == 0:
                        row["niveles_vivos"] = live_levels_lived(mono, it["cues"])
                rows.append(row)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"par": tag, "segundos_llenado": round(t_build, 1),
                               "segundos": round(time.time() - t0, 1), "filas": rows}, ensure_ascii=False))
    print(f"  {tag}: {len(rows)} filas (llenado {t_build:.0f}s, total {time.time()-t0:.0f}s)", flush=True)
    return str(out)


# ---------- agregación ----------

def oracle_reference(seeds):
    """d_nn y clase del especialista por consulta, desde exp11 (N=200)."""
    ref = {}
    for f in EXP11_RAW.glob("s*_N200_c*.json"):
        for r in json.loads(f.read_text(encoding="utf-8"))["texto"]:
            if r["brazo"] == "T-oraculo" and r.get("responde") and r["semilla"] in seeds:
                ref.setdefault(r["query"], []).append(r["d_nn_truth"])
    return {q: float(np.mean(v)) for q, v in ref.items()}


def m8_reference(seeds):
    ref = {}
    for f in EXP11_RAW.glob("s*_N200_c*.json"):
        for r in json.loads(f.read_text(encoding="utf-8"))["texto"]:
            if r["brazo"] == "M" and r.get("responde") and r["semilla"] in seeds:
                ref.setdefault(r["query"], []).append(r["d_nn_truth"])
    return {q: float(np.mean(v)) for q, v in ref.items()}


def aggregate(seeds):
    from scipy.stats import spearmanr
    overlaps = json.loads((OUT_DIR / "solapamiento.json").read_text(encoding="utf-8"))
    oracle = oracle_reference(seeds)
    m8 = m8_reference(seeds)
    table = []
    for f in sorted(RAW_DIR.glob("*.json")):
        raw = json.loads(f.read_text(encoding="utf-8"))
        rows = [r for r in raw["filas"] if r["responde"]]
        if not rows:
            continue
        by_q = {}
        for r in rows:
            by_q.setdefault(r["query"], []).append(r)
        d_m2 = float(np.mean([r["d_nn_truth"] for r in rows]))
        d_or = float(np.mean([oracle[q] for q in by_q if q in oracle]))
        d_m8 = float(np.mean([m8[q] for q in by_q if q in m8]))
        ov = overlaps[raw["par"]]
        shared_rows = [r for r in rows if r.get("pista_compartida")]
        table.append({
            "par": raw["par"],
            "solap_izquierda": ov["izquierda"], "solap_latente": ov["latente"],
            "etiquetas_compartidas": len(ov["etiquetas_compartidas"]),
            "consultas": len(by_q), "responde": len(rows) / len(raw["filas"]),
            "d_M2": d_m2, "d_oraculo": d_or, "d_M8": d_m8, "brecha_M2": d_m2 - d_or, "brecha_M8": d_m8 - d_or,
            "clase_M2": float(np.mean([r["nn_ok"] for r in rows])),
            "compat_otro": float(np.mean([r["compat_otro"] for r in rows])),
            "clase_pista_compartida": float(np.mean([r["nn_ok"] for r in shared_rows])) if shared_rows else float("nan"),
            "niveles_vivos": float(np.mean([r["niveles_vivos"] for r in rows if "niveles_vivos" in r])),
        })
    table.sort(key=lambda t: t["solap_izquierda"])
    x_l = [t["solap_izquierda"] for t in table]; x_r = [t["solap_latente"] for t in table]
    y = [t["brecha_M2"] for t in table]; y_cls = [1 - t["clase_M2"] for t in table]
    stats = {
        "n_pares": len(table),
        "spearman_brecha_vs_solap_izquierda": list(map(float, spearmanr(x_l, y))),
        "spearman_brecha_vs_solap_latente": list(map(float, spearmanr(x_r, y))),
        "spearman_error_clase_vs_solap_izquierda": list(map(float, spearmanr(x_l, y_cls))),
        "spearman_brecha_vs_etiquetas_compartidas": list(map(float, spearmanr([t["etiquetas_compartidas"] for t in table], y))),
    }
    (OUT_DIR / "resumen.json").write_text(json.dumps({"pares": table, "estadisticos": stats, "semillas": list(seeds)},
                                                     indent=1, ensure_ascii=False), encoding="utf-8")
    return table, stats


def write_report(table, stats, seeds):
    L = ["# Experimento 12 — la ventaja de partir contra el solapamiento entre dominios", "",
         f"28 pares de clases. Para cada par, una EHAM única con las dos clases (M2, N=200, mismo llenado que exp11) "
         f"responde a las consultas reservadas de esas clases; semillas {list(seeds)}, {REPS} sorteos. Referencia: el "
         "especialista (T-oráculo de exp11) y la EHAM de ocho clases (M8 de exp11) sobre las mismas consultas y semillas. "
         "Solapamiento: Jaccard medio por coordenada de los soportes de las dos clases, en el lado de las etiquetas "
         "(homo L, 300×16) y en el latente (homo R, 64×32).", "",
         "## Predicción pre-registrada", "",
         "La brecha de fidelidad de M2 respecto del especialista crece con el solapamiento (Spearman ρ > 0, p < 0.05); "
         "con pares disjuntos la brecha es cercana a cero.", "",
         "## Resultado", "",
         "| estadístico | ρ | p |", "|---|---|---|"]
    for k, v in stats.items():
        if k.startswith("spearman"):
            L.append(f"| {k.replace('spearman_', '').replace('_', ' ')} | {v[0]:.2f} | {v[1]:.4f} |")
    L += ["", "| par | solap. etiquetas | solap. latente | etiq. compartidas | consultas | d M2 | d oráculo | d M8 | brecha M2 | brecha M8 | clase M2 | compat con la otra clase |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in table:
        L.append(f"| {t['par']} | {t['solap_izquierda']:.3f} | {t['solap_latente']:.3f} | {t['etiquetas_compartidas']} | "
                 f"{t['consultas']} | {t['d_M2']:.1f} | {t['d_oraculo']:.1f} | {t['d_M8']:.1f} | {t['brecha_M2']:+.1f} | "
                 f"{t['brecha_M8']:+.1f} | {100*t['clase_M2']:.1f} | {t['compat_otro']:.2f} |")
    L += ["", "## Archivos", "- `raw/<par>.json`: filas por consulta, semilla y sorteo",
          "- `solapamiento.json`: solapamientos por par", "- `resumen.json`: tabla y estadísticos",
          "- `fig1_brecha_vs_solapamiento.png`"]
    (OUT_DIR / "README.md").write_text("\n".join(L), encoding="utf-8")


def make_figure(table, stats):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    for ax, key, xl, st in ((axes[0], "solap_izquierda", "solapamiento de soportes, etiquetas (Jaccard medio)",
                             stats["spearman_brecha_vs_solap_izquierda"]),
                            (axes[1], "solap_latente", "solapamiento de soportes, latente (Jaccard medio)",
                             stats["spearman_brecha_vs_solap_latente"])):
        x = [t[key] for t in table]; y = [t["brecha_M2"] for t in table]
        ax.axhline(0, color="#c3c2b7", lw=1)
        ax.scatter(x, y, s=36, color="#2a78d6", zorder=3)
        for t in table:
            if t["etiquetas_compartidas"] or t["brecha_M2"] > np.percentile(y, 80):
                ax.annotate(t["par"], (t[key], t["brecha_M2"]), xytext=(4, 3), textcoords="offset points",
                            fontsize=7, color="#52514e")
        ax.set_xlabel(xl, fontsize=9); ax.set_ylabel("brecha de fidelidad: d(M2) − d(especialista)", fontsize=9)
        ax.set_title(f"Spearman ρ = {st[0]:.2f}, p = {st[1]:.3f}", fontsize=10, loc="left")
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Experimento 12: la brecha de la EHAM de dos clases crece con el solapamiento entre ellas",
                 fontsize=11, x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT_DIR / "fig1_brecha_vs_solapamiento.png", dpi=160)
    plt.close(fig)


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="42-46")
    ap.add_argument("--reps", type=int, default=REPS)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--pairs", default=None, help="pares a-b separados por coma (por defecto los 28)")
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    seeds = parse_seeds(args.seeds)

    if not args.report_only:
        print("Soportes y solapamientos desde el caché N=200...", flush=True)
        sup = supports_from_cache()
        shared = shared_labels()
        (OUT_DIR / "solapamiento.json").write_text(json.dumps(pair_overlaps(sup, shared), indent=1, ensure_ascii=False),
                                                   encoding="utf-8")
        sup_R = {c: sup[c]["R"] for c in CLASSES}
        print("Banco de texto...", flush=True)
        nlp = get_nlp()
        vectors = load_all_vectors(nlp)
        bank = load_bank(nlp, vectors)
        train, held = split_bank(bank, N_TEXT_TRAIN_PER_CLASS)
        bank = train + held
        held_idx = list(range(len(train), len(bank)))
        pairs = PAIRS if not args.pairs else [tuple(p.split("-")) for p in args.pairs.split(",")]
        jobs = [(p, seeds, args.reps) for p in pairs if not (RAW_DIR / f"{'-'.join(p)}.json").exists()]
        print(f"  {len(held_idx)} consultas reservadas · {len(jobs)} pares por correr · semillas {seeds}", flush=True)
        t0 = time.time()
        if jobs:
            if args.workers > 1:
                with Pool(processes=min(args.workers, len(jobs)), initializer=init_worker,
                          initargs=(bank, held_idx, shared, sup_R)) as pool:
                    for _ in pool.imap_unordered(run_pair, jobs, chunksize=1):
                        pass
            else:
                init_worker(bank, held_idx, shared, sup_R)
                for j in jobs:
                    run_pair(j)
        print(f"Corridas terminadas en {(time.time()-t0)/60:.1f} min", flush=True)

    table, stats = aggregate(seeds)
    write_report(table, stats, seeds)
    make_figure(table, stats)
    print(json.dumps(stats, indent=1))
    print(f"Salidas -> {OUT_DIR}")


if __name__ == "__main__":
    main()
