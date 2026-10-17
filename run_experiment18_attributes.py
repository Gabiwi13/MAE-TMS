"""
Experimento 18: heteroasociación con características visibles de la imagen.

Una memoria hetero por eje y clase (patrón, techo, pelo; el color ya se midió
en exp17 con este mismo procedimiento). Cada vista se registra con el valor
que su objeto tiene en ese eje, según caracteristicas_borrador.json (aprobado
el 17 oct 2026). Solo objetos claros en el eje.

Pliegue 0: 41 vistas de test y hasta 200 de llenado de los mismos objetos.
Leave-object-out completo: un pliegue por objeto claro; se llena con los demás
y se evalúan sus 41 vistas. Lecturas: soporte y soporte normalizado por la
marginal de la memoria (exp17), las dos reportadas.

Uso:
  python run_experiment18_attributes.py --workers 10
  python run_experiment18_attributes.py --report-only
"""
import argparse
import contextlib
import io
import json
import os
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")   # antes de numpy: un hilo por proceso
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from run_experiment17_specific_word import (  # noqa: E402
    CLASSES, LAT_PATH, IDX_PATH, N_FILL_B, N_TEST_B, SEED_B, M_LABEL, P_LATENT, Q_LATENT, N_LAB,
    object_id, load_global_stats, quantize_latent_global, quantize_binary, _norm_weights,
    support_ranking, label_marginal, normalized_support)

ROOT = Path(__file__).parent
OUT_DIR = ROOT / "results" / "experimento18"
LABELS = OUT_DIR / "caracteristicas_borrador.json"
VECS = OUT_DIR / "attribute_vectors.json"
MODELS = OUT_DIR / "modelos"            # solo pliegue 0, fuera de git
RAW = OUT_DIR / "filas.json"


def labels():
    return json.loads(LABELS.read_text(encoding="utf-8"))


def axes_of(cls):
    lab = labels().get(cls, {})
    return sorted({ax for o in lab.values() for ax in o})


def value_of(cls, axis, path):
    v = labels()[cls].get(str(object_id(path)), {}).get(axis)
    return v[0] if v and v[1] else None


def word_vectors_q():
    raw = json.loads(VECS.read_text())
    return {w: quantize_binary(np.asarray(v, dtype=float), M_LABEL) for w, v in raw.items()}


def split(index, cls, axis, fold):
    """fold 0: objetos conocidos; fold = id de objeto: ese objeto queda fuera."""
    idx = [i for i, p in enumerate(index[cls]) if value_of(cls, axis, p)]
    rng = np.random.RandomState(SEED_B + CLASSES.index(cls) + 1000 * fold)
    if fold == 0:
        idx = np.array(idx)
        rng.shuffle(idx)
        return {"test": idx[:N_TEST_B].tolist(), "llenado": idx[N_TEST_B:N_TEST_B + N_FILL_B].tolist()}
    rest = np.array([i for i in idx if object_id(index[cls][i]) != fold])
    rng.shuffle(rest)
    return {"nuevo": [i for i in idx if object_id(index[cls][i]) == fold], "llenado": rest[:N_FILL_B].tolist()}


def jobs():
    index = json.loads(IDX_PATH.read_text())
    out = []
    for cls in CLASSES:
        for axis in axes_of(cls):
            objs = sorted({object_id(p) for p in index[cls] if value_of(cls, axis, p)})
            out += [(axis, cls, 0)] + [(axis, cls, o) for o in objs]
    return out


def run_job(job):
    """Llena la memoria del pliegue y la evalúa en el mismo proceso."""
    import pickle
    from hetero_memory import HeteroAssociativeMemory
    from associative_memory import HomoAssociativeMemory
    from stage5_fill import FILL_VARIANTS
    axis, cls, fold = job
    t0 = time.time()
    arr = np.load(LAT_PATH, mmap_mode="r")
    index = json.loads(IDX_PATH.read_text())
    g = tuple(x.astype(np.float32) for x in load_global_stats())
    ci = CLASSES.index(cls)
    wq = word_vectors_q()
    sp = split(index, cls, axis, fold)
    own = sorted({value_of(cls, axis, index[cls][i]) for i in sp["llenado"]})
    with contextlib.redirect_stdout(io.StringIO()):
        mem_H = HeteroAssociativeMemory(N_LAB, M_LABEL, P_LATENT, Q_LATENT)
        mem_R = HomoAssociativeMemory(P_LATENT, Q_LATENT)
        for i in sp["llenado"]:
            w_q = wq[value_of(cls, axis, index[cls][i])]
            for v in range(FILL_VARIANTS):
                z_q = quantize_latent_global(np.asarray(arr[ci, i, v]), *g, Q_LATENT)
                mem_H.register(w_q, z_q)
                mem_R.register(z_q)
    if fold == 0:
        MODELS.mkdir(parents=True, exist_ok=True)
        with open(MODELS / f"{axis}_{cls}.pkl", "wb") as f:
            pickle.dump((mem_H, mem_R), f)
    fill_vals = [value_of(cls, axis, index[cls][i]) for i in sp["llenado"]]
    v, n = np.unique(fill_vals, return_counts=True)
    base = str(v[np.argmax(n)])
    marg = label_marginal(mem_H)
    rows = []
    for bank in [b for b in sp if b != "llenado"] + ["llenado"]:
        if fold and bank == "llenado":
            continue
        for i in sp[bank][:N_TEST_B]:
            path = index[cls][i]
            z_q = quantize_latent_global(np.asarray(arr[ci, i, 0]), *g, Q_LATENT)
            row = {"eje": axis, "clase": cls, "pliegue": fold, "banco": bank, "imagen": Path(path).name,
                   "objeto": object_id(path), "verdad": value_of(cls, axis, path), "valores_agente": own,
                   "base": base}
            with contextlib.redirect_stdout(io.StringIO()):
                proj = mem_H.project(mem_H.validate(z_q, 1), _norm_weights(mem_R.recog_weights(z_q), P_LATENT), 1)
            row["reconoce"] = bool(np.count_nonzero(np.sum(proj, axis=1) == 0) == 0)
            if row["reconoce"]:
                row["soporte"] = support_ranking(proj, own, wq)
                row["soporte_norm"] = normalized_support(proj, marg, own, wq)
            rows.append(row)
    return {"job": job, "segundos": round(time.time() - t0), "filas": rows}


def _acc(rs, key):
    rs = [r for r in rs if r["reconoce"]]
    return sum(r[key][0][0] == r["verdad"] for r in rs), len(rs)


def report():
    data = json.loads(RAW.read_text())
    rows = [r for d in data for r in d["filas"]]
    lines = ["Experimento 18: una memoria hetero por eje y clase; agente de la clase verdadera.",
             "Top-1 sobre vistas reconocidas. base = el valor más registrado del agente."]
    for axis in sorted({r["eje"] for r in rows}):
        lines.append(f"\n=== eje {axis} ===")
        for bank, label in (("test", "objetos conocidos, vistas nuevas"), ("llenado", "vistas del llenado"),
                            ("nuevo", "objetos nuevos (leave-object-out)")):
            rs = [r for r in rows if r["eje"] == axis and r["banco"] == bank]
            if not rs:
                continue
            rec = [r for r in rs if r["reconoce"]]
            parts = []
            for key in ("soporte", "soporte_norm"):
                ok, n = _acc(rs, key)
                bal = np.mean([np.mean([r[key][0][0] == c for r in rec if r["verdad"] == c])
                               for c in {r["verdad"] for r in rec}]) if rec else float("nan")
                parts.append(f"{key} {100 * ok / max(n, 1):5.1f} % (bal. {100 * bal:5.1f})")
            b = sum(r["verdad"] == r["base"] for r in rec)
            lines.append(f"  [{label}] vistas {len(rs)}, reconocidas {len(rec)} · " + " · ".join(parts) +
                         f" · base {100 * b / max(len(rec), 1):5.1f} %")
        nuevo = [r for r in rows if r["eje"] == axis and r["banco"] == "nuevo"]
        if nuevo:
            lines.append("  por objeto nuevo (valor · ¿mayoritario en el agente? · reconocidas · soporte · norm):")
            for cls in CLASSES:
                for o in sorted({r["objeto"] for r in nuevo if r["clase"] == cls}):
                    rs = [r for r in nuevo if r["clase"] == cls and r["objeto"] == o]
                    rec = [r for r in rs if r["reconoce"]]
                    a, _ = _acc(rs, "soporte")
                    b, _ = _acc(rs, "soporte_norm")
                    mayor = rs[0]["verdad"] == rs[0]["base"]
                    imposible = rs[0]["verdad"] not in rs[0]["valores_agente"]
                    lines.append(f"    {cls}{o:<3} {rs[0]['verdad']:<11} {'sí' if mayor else 'NO':<3} "
                                 f"{len(rec):>2}/{len(rs)}  {a:>2}  {b:>2}" +
                                 ("   (imposible: el agente no tiene ese valor)" if imposible else ""))
            for mayor in (True, False):
                rs = [r for r in nuevo if (r["verdad"] == r["base"]) == mayor and r["verdad"] in r["valores_agente"]]
                if rs:
                    a, n = _acc(rs, "soporte")
                    b, _ = _acc(rs, "soporte_norm")
                    lines.append(f"  objetos nuevos con valor {'mayoritario' if mayor else 'minoritario'}: "
                                 f"soporte {100 * a / max(n, 1):5.1f} % · norm {100 * b / max(n, 1):5.1f} % (n={n}, sin imposibles)")
    text = "\n".join(lines)
    (OUT_DIR / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--only", default="", help="eje:clase:pliegue,... para una prueba")
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    if not args.report_only:
        todo = jobs()
        if args.only:
            want = {tuple(x.split(":")) for x in args.only.split(",")}
            todo = [j for j in todo if (j[0], j[1], str(j[2])) in want]
        done = json.loads(RAW.read_text()) if RAW.exists() else []
        hecho = {tuple(d["job"]) for d in done}
        todo = [j for j in todo if j not in hecho]
        print(f"{len(todo)} pliegues por correr ({len(hecho)} ya hechos), {args.workers} procesos", flush=True)
        t0 = time.time()
        with Pool(args.workers) as pool:
            for k, res in enumerate(pool.imap_unordered(run_job, todo), 1):
                done.append(res)
                RAW.write_text(json.dumps(done, ensure_ascii=False))
                print(f"  {k}/{len(todo)} {tuple(res['job'])} en {res['segundos']} s ({time.time() - t0:.0f} s)",
                      flush=True)
    report()


if __name__ == "__main__":
    main()
