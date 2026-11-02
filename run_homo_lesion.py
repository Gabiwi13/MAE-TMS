"""
E. ¿Qué hace una homo que la hetero con borde no? Dos arquitecturas con los
mismos datos: B (la hetero recibe 100 de las 200 imágenes de llenado con su
palabra; la homo latente, todas) y A (una sola hetero: las otras 100 van a su
borde y la homo se lee de ella). Parte 1 sin lesión; parte 2 destruyendo una
fracción de las celdas de la hetero. Predicciones y regla de decisión en
results/homo_marginal/README.md (E), escritas antes de correr. Las memorias
viven en RAM; no toca models/. Un subproceso por agente.
"""
import contextlib
import copy
import io
import json
import pickle
import random
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from associative_memory import HomoAssociativeMemory
from hetero_lib import commons
from hetero_lib.associative import AssociativeMemory
from hetero_memory import _norm_weights
from relleno_paralelo import _fill, spec

OUT = ROOT / "results" / "homo_marginal"
FRACTIONS = (0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0)
N_PAIRED = 100           # imágenes emparejadas de las 200 de llenado
VARIANTS = 16
M_LABEL = 16
MAX_PROCS = 4            # por la memoria libre de la máquina
SETS = ("pareadas", "sin_pareja", "test")


def homo_from(table, like):
    """Como run_homo_marginal.homo_from, sin importar torch en el subproceso."""
    am = like._am
    es = commons.ExperimentSettings(iota=am.iota, kappa=am.kappa, xi=am.xi, sigma=am.sigma)
    h = HomoAssociativeMemory(like.n, like.m, iota=am.iota, kappa=am.kappa, xi=am.xi, sigma=am.sigma)
    with contextlib.redirect_stdout(io.StringIO()):
        h._am = AssociativeMemory.from_relation(table, es)
    return h


def view(h, like):
    """Homo latente leída de la hetero: borde + marginal, sin el 1 fijo del borde."""
    table = h._relation[0, :, :, :h.q].sum(axis=1).astype(np.int64) - 1
    return homo_from(table, like)


def lesion(h, mask, mode):
    """Copia de h con las celdas de mask destruidas ('azar') o con su conteo
    pasado a los dos bordes ('desasociar')."""
    g = copy.deepcopy(h)
    m, q = g.m, g.q
    rel = g._relation
    inner = mask[:, :, :m, :q]
    if mode == "desasociar":
        moved = np.where(inner, rel[:, :, :m, :q], 0)
        rel[:, :, m, :q] += moved.sum(axis=2)      # imagen sin palabra
        rel[:, :, :m, q] += moved.sum(axis=3)      # palabra sin imagen
    else:
        rel[:, :, m, :q][mask[:, :, m, :q]] = 1    # el borde vuelve a su 1 fijo
        rel[:, :, :m, q][mask[:, :, :m, q]] = 1
    rel[:, :, :m, :q][inner] = 0
    with contextlib.redirect_stdout(io.StringIO()):
        g._updated = g.update()
    return g


def familiar(homo, z):
    """Como stage7.recognize_gated_right: contención estricta en la homo."""
    return bool(np.all(homo.recog_weights(z) > 0))


def evaluate(h, homo, queries, others, vocab, words_of_class, keep_recall):
    """Nombrar se lee de la proyección imagen → texto: el recuerdo oficial se
    reconoce si y solo si ninguna columna queda vacía (el muestreo no rechaza
    después). Las palabras se evocan del prototipo (el valor más probable por
    coordenada) y no del muestreo, que tarda ~22 s por imagen."""
    words, mat, norms = vocab
    out = {}
    for name in SETS:
        rows = []
        for z in queries[name]:
            fam = familiar(homo, z)
            w = _norm_weights(homo.recog_weights(z), len(z))
            with contextlib.redirect_stdout(io.StringIO()):
                proj = h.project(h.validate(z, 1), w, 1)
            ok = not np.any(proj.sum(axis=1) == 0)
            good = False
            proto = None
            if ok:
                proto = np.argmax(proj, axis=1)
                rc = proto.astype(float) / (M_LABEL - 1) * 2.0 - 1.0
                sims = mat @ rc / (norms * np.linalg.norm(rc) + 1e-8)
                good = any(words[i] in words_of_class for i in np.argsort(-sims)[:3])
            row = {"familiar": fam, "nombra": bool(ok), "nombra_bien": bool(good)}
            if keep_recall:
                row["recuerdo"] = None if proto is None else proto.tolist()
            rows.append(row)
        out[name] = rows
    out["ajenas_aceptadas"] = int(sum(familiar(homo, z) for z in others))
    return out


def complete(homo, unpaired_q):
    """Mitad de las coordenadas indefinidas; error en las ocultas contra la
    imagen original y contra la siguiente imagen sin pareja del agente."""
    rows = []
    n = len(unpaired_q)
    for k, z in enumerate(unpaired_q):
        hide = np.random.default_rng(50_000 + k).choice(len(z), len(z) // 2, replace=False)
        cue = z.astype(float)
        cue[hide] = np.nan
        random.seed(60_000 + k)
        with contextlib.redirect_stdout(io.StringIO()):
            r, ok, _ = homo.recall(cue)
        if not ok:
            rows.append(None)
            continue
        other = unpaired_q[(k + 1) % n]
        rows.append({"error_propia": float(np.mean(np.abs(r[hide] - z[hide]))),
                     "error_otra": float(np.mean(np.abs(r[hide] - other[hide])))})
    return rows


def run_agent(job):
    t0 = time.time()

    def log(msg):
        print(f"[{job['cls']}] {msg}: {time.time() - t0:.0f} s", file=sys.stderr, flush=True)

    nan_word = np.full(len(job["paired"][0][0]), np.nan)
    hB = _fill(job["spec"], job["paired"])
    hA = copy.deepcopy(hB)                 # registrar es sumar: A = B + lo sin pareja
    with contextlib.redirect_stdout(io.StringIO()):
        for z in job["unpaired"]:
            hA.register(nan_word, z)
    homo_R = job["homo_R"]
    vA = view(hA, homo_R)
    checks = {
        "interior_A_igual_a_B": bool(np.array_equal(hA.relation, hB.relation)),
        "lectura_A_igual_a_homo_oficial": bool(np.array_equal(
            np.asarray(vA._am.relation), np.asarray(homo_R._am.relation))),
        "segundos_llenado": round(time.time() - t0, 1)}
    log("llenado")
    args = (job["queries"], job["others"], job["vocab"], job["words_of_class"])
    res = {"agente": job["cls"], "chequeos": checks,
           "f0": {"B": evaluate(hB, homo_R, *args, keep_recall=True),
                  "A": evaluate(hA, vA, *args, keep_recall=True)},
           "completar": {"B": complete(homo_R, job["queries"]["sin_pareja"]),
                         "A": complete(vA, job["queries"]["sin_pareja"])},
           "lesion": {}}
    log("sin lesión")
    ci = job["ci"]
    for f in job["fractions"]:
        mask = np.random.default_rng(7_000 + 100 * ci + int(f * 100)).random(hA._relation.shape) < f
        mask_R = np.random.default_rng(8_000 + 100 * ci + int(f * 100)).random(
            np.asarray(homo_R._am.relation).shape) < f
        table = np.asarray(homo_R._am.relation, dtype=np.int64).copy()
        table[mask_R] = 0
        homo_dam = homo_from(table, homo_R)
        hB_f = lesion(hB, mask, "azar")
        cond = {"B focal": evaluate(hB_f, homo_R, *args, keep_recall=False),
                "B global": evaluate(hB_f, homo_dam, *args, keep_recall=False)}
        del hB_f
        hA_f = lesion(hA, mask, "azar")
        cond["A al azar"] = evaluate(hA_f, view(hA_f, homo_R), *args, keep_recall=False)
        del hA_f
        hA_d = lesion(hA, mask, "desasociar")
        vd = view(hA_d, homo_R)
        cond["A desasociar"] = evaluate(hA_d, vd, *args, keep_recall=False)
        cond["chequeo_desasociar_lectura_intacta"] = bool(np.array_equal(
            np.asarray(vd._am.relation), np.asarray(vA._am.relation)))
        del hA_d, mask
        res["lesion"][str(f)] = cond
        log(f"lesión {f}")
    res["segundos"] = round(time.time() - t0, 1)
    return res


def run_all(jobs):
    tmp = Path(tempfile.mkdtemp())
    try:
        out = {}
        for k in range(0, len(jobs), MAX_PROCS):
            procs = {}
            for job in jobs[k:k + MAX_PROCS]:
                c = job["cls"]
                (tmp / f"{c}.job").write_bytes(pickle.dumps(job))
                procs[c] = subprocess.Popen([sys.executable, __file__, "--agente",
                                             str(tmp / f"{c}.job"), str(tmp / f"{c}.out")])
            for c, pr in procs.items():
                if pr.wait() != 0:
                    raise RuntimeError(f"falló el agente {c}")
                out[c] = pickle.loads((tmp / f"{c}.out").read_bytes())
                print(f"{c}: {out[c]['segundos']} s, {out[c]['chequeos']}", flush=True)
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def tally(rows):
    n = len(rows)
    fam = sum(r["familiar"] for r in rows)
    nom = sum(r["nombra"] for r in rows)
    return {"n": n, "familiar": fam, "nombra": nom,
            "nombra_bien": sum(r["nombra_bien"] for r in rows),
            "nombra_y_familiar": sum(r["familiar"] and r["nombra"] for r in rows),
            "reconoce_sin_nombrar": sum(r["familiar"] and not r["nombra"] for r in rows),
            "nombra_sin_familiar": sum(r["nombra"] and not r["familiar"] for r in rows),
            "rechaza": sum(not r["familiar"] and not r["nombra"] for r in rows)}


def summarize(results, n_others):
    def cond_sum(get):
        s = {name: tally([r for res in results.values() for r in get(res)[name]]) for name in SETS}
        s["ajenas"] = {"n": n_others, "aceptadas": sum(get(res)["ajenas_aceptadas"]
                                                       for res in results.values())}
        return s

    summary = {"chequeos": {c: r["chequeos"] for c, r in results.items()},
               "sin_lesion": {k: cond_sum(lambda res, k=k: res["f0"][k]) for k in ("B", "A")}}
    same = {}
    for name in SETS:
        d = {"familiar_distinto": 0, "nombra_distinto": 0, "recuerdo_distinto": 0, "n": 0}
        for res in results.values():
            for a, b in zip(res["f0"]["A"][name], res["f0"]["B"][name]):
                d["n"] += 1
                d["familiar_distinto"] += a["familiar"] != b["familiar"]
                d["nombra_distinto"] += a["nombra"] != b["nombra"]
                d["recuerdo_distinto"] += a["recuerdo"] != b["recuerdo"]
        same[name] = d
    summary["A_contra_B_sin_lesion"] = same

    comp = {}
    for k in ("B", "A"):
        rows = [r for res in results.values() for r in res["completar"][k]]
        ok = [r for r in rows if r is not None]
        comp[k] = {"n": len(rows), "reconocidas": len(ok),
                   "error_medio_contra_la_original": float(np.mean([r["error_propia"] for r in ok])),
                   "error_medio_contra_otra": float(np.mean([r["error_otra"] for r in ok])),
                   "mas_cerca_de_la_original": sum(r["error_propia"] < r["error_otra"] for r in ok),
                   "mas_cerca_de_otra": sum(r["error_propia"] > r["error_otra"] for r in ok)}
    summary["completar"] = comp

    les = {}
    first = next(iter(results.values()))
    for f in first["lesion"]:
        les[f] = {k: cond_sum(lambda res, f=f, k=k: res["lesion"][f][k])
                  for k in ("B focal", "B global", "A al azar", "A desasociar")}
        les[f]["desasociar_lectura_intacta"] = sum(
            res["lesion"][f]["chequeo_desasociar_lectura_intacta"] for res in results.values())
    summary["lesion"] = les
    return summary


def main(trial):
    import run_homo_marginal as hm
    from run_homo_sin_pareja import fill_q, test_images
    from stage5_fill import build_label_sequence

    s6, s7 = hm.s6, hm.s7
    with contextlib.redirect_stdout(io.StringIO()):
        agents = s6.load_agents()
    g_min, g_max = s7.load_global_stats()
    images = test_images(g_min, g_max)
    label_vecs = s6.load_all_vectors()
    all_vecs = {}
    for c in s6.CLASSES:
        all_vecs.update(label_vecs[c])
    words = list(all_vecs)
    mat = np.array([all_vecs[w] for w in words], dtype=np.float64)
    vocab = (words, mat, np.linalg.norm(mat, axis=1))

    classes = ["apple"] if trial else list(s6.CLASSES)
    n_q = 10 if trial else None
    jobs = []
    for c in classes:
        ci = s6.CLASSES.index(c)
        lat = fill_q(c, g_min, g_max)
        seq = build_label_sequence(c)
        k = N_PAIRED * VARIANTS
        own = [z for cj, z in images if cj == ci]
        jobs.append({
            "cls": c, "ci": ci, "spec": spec(agents[c].mem_dom_H),
            "paired": [(seq[i % len(seq)], z) for i, z in enumerate(lat[:k])],
            "unpaired": lat[k:], "homo_R": agents[c].mem_dom_R,
            "queries": {"pareadas": [lat[b * VARIANTS] for b in range(N_PAIRED)][:n_q],
                        "sin_pareja": [lat[b * VARIANTS] for b in range(N_PAIRED, 2 * N_PAIRED)][:n_q],
                        "test": own[:n_q]},
            "others": [z for cj, z in images if cj != ci],
            "vocab": vocab, "words_of_class": set(label_vecs[c]),
            "fractions": (0.5,) if trial else FRACTIONS})
    n_others = sum(len(j["others"]) for j in jobs)
    del agents
    results = run_all(jobs)
    summary = summarize(results, n_others)
    if trial:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "lesion.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False),
                                     encoding="utf-8")
    (OUT / "lesion_agentes.json").write_text(json.dumps(results, ensure_ascii=False),
                                             encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--agente":
        job = pickle.loads(Path(sys.argv[2]).read_bytes())
        Path(sys.argv[3]).write_bytes(pickle.dumps(run_agent(job)))
    else:
        main(trial="--prueba" in sys.argv)
