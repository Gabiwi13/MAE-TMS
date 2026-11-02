"""Calibración con conjunto de evaluación fijo (jurado M2). Usa la lógica de
run_ablation.py sin cambios; solo cambia qué consultas forman el directorio y
cuáles se evalúan. Diseño en README.md.

Uso:  python results/calibracion_evaluacion_fija/calibracion_fija.py
"""
import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import run_ablation as abl
from eval_bank import ALL_QUERIES, GROUND_TRUTH
from stage6_interaction import CLASSES, get_nlp, load_all_vectors, tokenize_query, prevectorize

PER_CLASS_EVAL = 15
EVAL_SEEDS = (0, 1, 2, 3, 4)
SEEDS = (0, 1, 2, 3, 4)
CONDS = ("A", "B1", "D", "G")
T_975_4 = 2.776
K = len(CLASSES)


def eval_split(eval_seed):
    rng = np.random.RandomState(eval_seed)
    E = []
    for c in CLASSES:
        idx = [i for i, g in enumerate(GROUND_TRUTH) if g == c]
        E.extend(sorted(rng.choice(idx, PER_CLASS_EVAL, replace=False).tolist()))
    E = sorted(E)
    eset = set(E)
    R = [i for i in range(len(ALL_QUERIES)) if i not in eset]
    return E, R


def formation(R, N, seed, stratified):
    rng = np.random.RandomState(100 + seed)
    if not stratified:
        return [int(i) for i in rng.permutation(R)[:N]]
    per = N // K
    pools = []
    for c in CLASSES:
        pool = [i for i in R if GROUND_TRUTH[i] == c]
        rng.shuffle(pool)
        pools.append(pool[:per])
    out = []
    for j in range(per):
        for pool in pools:
            if j < len(pool):
                out.append(pool[j])
    return out


def run_one(cond, form_idx, E, seed, mdoms, nlp, vectors):
    mdir_class, m_mdir, kw, predict_fn, _, _ = abl.get_condition_config(cond)
    agents, tme = abl.make_agents(mdoms, mdir_class, m_mdir, kw)
    fq = [ALL_QUERIES[i] for i in form_idx]
    early_f = abl.run_early_phase(fq, agents, tme, nlp, vectors, m_mdir)
    rng = np.random.RandomState(seed * 1000 + 42)
    mature = abl.run_mature_phase([ALL_QUERIES[i] for i in E], agents, nlp, vectors,
                                  rng, predict_fn, m_mdir)
    counts = agents[CLASSES[0]].mem_dir.agent_counts.tolist()
    return early_f, mature, counts


def stats(v):
    v = np.asarray(v, dtype=float)
    m, sd = float(v.mean()), float(v.std(ddof=1)) if len(v) > 1 else 0.0
    h = T_975_4 * sd / np.sqrt(len(v)) if len(v) == 5 else float("nan")
    return {"media": round(m, 2), "de": round(sd, 2), "min": round(float(v.min()), 2),
            "max": round(float(v.max()), 2), "ic95_t": [round(m - h, 2), round(m + h, 2)]}


def main():
    t0 = time.time()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    nlp = get_nlp()
    vectors = load_all_vectors(nlp)
    toks = {}
    for q in ALL_QUERIES:
        toks[q] = tokenize_query(q, nlp)
    prevectorize(vectors, set(t for ts in toks.values() for t in ts), allow_fallback=False)
    mdoms = abl.load_base_mdoms()
    has_name = [int(g in toks[q]) for q, g in zip(ALL_QUERIES, GROUND_TRUTH)]

    # control: lógica original
    ctrl = {}
    for cond in ("A", "B1"):
        m = abl.run_single_experiment(cond, 400, 0, mdoms, None, nlp, vectors)
        ctrl[cond] = {"temprana": round(100 * m["early_acc"], 2), "madura": round(100 * m["mature_acc"], 2)}
    print(f"Control (lógica original, N=400): {ctrl}  ({time.time()-t0:.1f}s)", flush=True)

    rows, per_query = [], {}
    timing = {}
    for es in EVAL_SEEDS:
        te = time.time()
        E, R = eval_split(es)
        n_max = len(R)
        Ns = (50, 100, 200, n_max)
        gtE = [GROUND_TRUTH[i] for i in E]
        # temprana sobre E: agentes desechables, nada de E se registra en los que se evalúan
        mdir_class, m_mdir, kw, *_ = abl.get_condition_config("A")
        ag0, tme0 = abl.make_agents(mdoms, mdir_class, m_mdir, kw)
        early_E = abl.run_early_phase([ALL_QUERIES[i] for i in E], ag0, tme0, nlp, vectors, m_mdir)
        early_ok = [int(e == g) for e, g in zip(early_E, gtE)]
        early_acc = 100 * np.mean(early_ok)
        print(f"E (semilla {es}): {len(E)} consultas, {sum(has_name[i] for i in E)} con nombre de clase, "
              f"temprana {early_acc:.2f} %; R = {n_max}", flush=True)
        for cond in CONDS:
            strat = cond in ("D", "G")
            for N in Ns:
                for s in SEEDS:
                    form_idx = formation(R, N, s, strat)
                    assert not set(form_idx) & set(E)
                    early_f, mature, counts = run_one(cond, form_idx, E, s, mdoms, nlp, vectors)
                    mat_ok = [int(m == g) for m, g in zip(mature, gtE)]
                    gtF = [GROUND_TRUTH[i] for i in form_idx]
                    row = {"semilla_E": es, "condicion": cond, "N": N, "N_real": len(form_idx), "semilla": s,
                           "temprana_E": round(early_acc, 3),
                           "madura_E": round(100 * np.mean(mat_ok), 3),
                           "fidelidad_E": round(100 * np.mean([m == e for m, e in zip(mature, early_E)]), 3),
                           "dif_madura_menos_temprana": round(100 * np.mean(mat_ok) - early_acc, 3),
                           "rechazo_madura_E": sum(m == "REJ" for m in mature),
                           "temprana_formacion": round(100 * np.mean([e == g for e, g in zip(early_f, gtF)]), 3),
                           "con_nombre_formacion_pct": round(100 * np.mean([has_name[i] for i in form_idx]), 2),
                           "registros_por_agente": counts}
                    rows.append(row)
                    per_query[(es, cond, N, s)] = mat_ok
        per_query[(es, "early")] = early_ok
        timing[f"semilla_E_{es}_s"] = round(time.time() - te, 1)
        print(f"  semilla E {es}: {timing[f'semilla_E_{es}_s']}s", flush=True)

    # agregados
    summary = {"control_logica_original_N400_semilla0": ctrl, "por_semilla_E": {}}
    for es in EVAL_SEEDS:
        E, R = eval_split(es)
        Ns = (50, 100, 200, len(R))
        d = {"n_E": len(E), "con_nombre_E": sum(has_name[i] for i in E), "n_R": len(R),
             "temprana_E": round(100 * np.mean(per_query[(es, "early")]), 2), "condiciones": {}}
        for cond in CONDS:
            for N in Ns:
                sub = [r for r in rows if r["semilla_E"] == es and r["condicion"] == cond and r["N"] == N]
                entry = {k: stats([r[k] for r in sub]) for k in
                         ("madura_E", "dif_madura_menos_temprana", "fidelidad_E", "temprana_formacion",
                          "con_nombre_formacion_pct")}
                entry["N_real"] = sorted(set(r["N_real"] for r in sub))
                if es == 0:
                    diffs = np.mean([np.array(per_query[(es, cond, N, s)]) for s in SEEDS], axis=0) \
                        - np.array(per_query[(es, "early")])
                    rng = np.random.RandomState(7)
                    boot = [100 * diffs[rng.randint(0, len(diffs), len(diffs))].mean() for _ in range(2000)]
                    entry["dif_bootstrap_E_ic95"] = [round(float(np.percentile(boot, 2.5)), 2),
                                                     round(float(np.percentile(boot, 97.5)), 2)]
                d["condiciones"][f"{cond}_N{N}"] = entry
        summary["por_semilla_E"][str(es)] = d

    secs = round(time.time() - t0, 1)
    summary["segundos"] = secs
    summary["tiempos"] = timing
    with open(OUT / "filas.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    (OUT / "resumen.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "por_consulta_E0.json").write_text(json.dumps(
        {"E": [ALL_QUERIES[i] for i in eval_split(0)[0]],
         "temprana": per_query[(0, "early")],
         "madura": {f"{c}_N{N}_s{s}": v for (es, c, N, s), v in
                    ((k, v) for k, v in per_query.items() if len(k) == 4 and k[0] == 0)}},
        ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary["por_semilla_E"]["0"], indent=1, ensure_ascii=False))
    print(f"Tiempo total {secs}s")


if __name__ == "__main__":
    main()
