"""
C. Emparejamiento desigual: la homo de etiquetas queda como la oficial y la
hetero se llena con otro reparto de palabras sobre los mismos latentes.
  C1: todas las palabras emparejadas, en proporción a 1/rango.
  C2: solo la primera mitad de las palabras emparejadas.
Se compara el sistema con los pesos de la homo y con los de la marginal de la
nueva hetero. Las memorias viven en RAM; no toca models/. Criterio en
plan_cierre_pesos_homo.md (29 oct).
"""
import contextlib
import io
import json
import pickle
import shutil
import tempfile
from pathlib import Path

import numpy as np

import run_homo_marginal as hm
from eval_bank import GROUND_TRUTH
from quantizer import quantize_binary
from relleno_paralelo import rebuild_heteros
from run_homo_sin_pareja import fill_q
from run_pesos_recuerdo import SEEDS, bank_cues, run_passes
from stage5_fill import M, ROOT

s6, s7 = hm.s6, hm.s7
CLASSES = hm.CLASSES


def words(c):
    """Palabras distintas en el orden del archivo, con frecuencia y vector cuantizado."""
    labels = json.loads((ROOT / f"labels_{c}.json").read_text())
    raw = json.loads((ROOT / f"label_vectors_{c}.json").read_text())
    return [(w, int(f), quantize_binary(np.array(raw[w], dtype=np.float32), M))
            for w, f in labels.items() if w in raw]


def seq_c1(ws, total):
    r = 1.0 / np.arange(1, len(ws) + 1)
    counts = np.maximum(1, np.floor(total * r / r.sum())).astype(int)
    counts[0] += total - counts.sum()
    return [v for (_, _, v), k in zip(ws, counts) for _ in range(k)]


def seq_c2(ws):
    return [v for _, f, v in ws[: (len(ws) + 1) // 2] for _ in range(f)]


def text_decisions(agents, cues_by_q):
    rows = []
    rng = np.random.RandomState(42)
    for cues in cues_by_q:
        entry = s6.AGENT_LIST[int(rng.randint(len(s6.AGENT_LIST)))]
        scores = np.array([[agents[c].recognize_gated(v) for c in CLASSES] for v in cues]) \
            if cues else np.zeros((0, len(CLASSES)))
        tot = scores.sum(axis=0) if cues else np.zeros(len(CLASSES))
        early = int(np.argmax(tot)) if tot.sum() > 0 else -1
        widx, gate = -1, False
        if cues:
            widx, *_ = s6.route_transactive(entry, agents, cues, modality="text")
            if widx >= 0:
                gate = bool(scores[:, widx].max() > 0)
        homo_cont = [[bool(agents[c].mem_dom_L.recog_weights(v).min() > 0) for c in CLASSES]
                     for v in cues]
        rows.append({"scores": scores, "early": early, "dest": widx, "gate": gate,
                     "homo_contiene": np.array(homo_cont, dtype=bool).reshape(-1, len(CLASSES))})
    return rows


def summarize(rows, truth):
    pairs = sum(r["scores"].size for r in rows)
    return {"pares_pista_agente": pairs,
            "la_homo_de_etiquetas_contiene": int(sum(r["homo_contiene"].sum() for r in rows)),
            "la_compuerta_de_la_hetero_pasa": int(sum((r["scores"] > 0).sum() for r in rows)),
            "ganador_temprano_acierto_pct":
                100 * float(np.mean([r["early"] == t for r, t in zip(rows, truth)])),
            "rechazadas_temprano": sum(r["early"] < 0 for r in rows)}


def diff(a, b):
    return {"contencion_de_la_homo_distinta":
                int(sum((x["homo_contiene"] != y["homo_contiene"]).sum() for x, y in zip(a, b))),
            "compuerta_hetero_distinta":
                int(sum(((x["scores"] > 0) != (y["scores"] > 0)).sum() for x, y in zip(a, b))),
            "ganador_temprano_distinto": sum(x["early"] != y["early"] for x, y in zip(a, b)),
            "destino_maduro_distinto": sum(x["dest"] != y["dest"] for x, y in zip(a, b)),
            "compuerta_madura_distinta": sum(x["gate"] != y["gate"] for x, y in zip(a, b))}


def main():
    hm.OUT.mkdir(parents=True, exist_ok=True)
    cues = bank_cues()
    with contextlib.redirect_stdout(io.StringIO()):
        agents = s6.load_agents()
    truth = [CLASSES.index(g) for g in GROUND_TRUTH]
    g_min, g_max = s7.load_global_stats()
    official = {c: (a.mem_dom_L, a.mem_dom_R, a.mem_dom_H) for c, a in agents.items()}
    tmp = Path(tempfile.mkdtemp())
    res, specs = {}, {}
    for cond in ("C1", "C2"):
        jobs = {}
        for c in CLASSES:
            lat = fill_q(c, g_min, g_max)
            ws = words(c)
            seq = seq_c1(ws, len(lat)) if cond == "C1" else seq_c2(ws)
            jobs[c] = (official[c][2], [(seq[i % len(seq)], z) for i, z in enumerate(lat)])
        heteros = rebuild_heteros(jobs)
        (tmp / f"{cond}.pkl").write_bytes(pickle.dumps(heteros))
        homos, margs = {}, {}
        for c in CLASSES:
            oL, oR, _ = official[c]
            agents[c].mem_dom_H = heteros[c]
            homos[c] = (oL, oR)
            margs[c] = (hm.marginal_homo(heteros[c], oL, 0), hm.marginal_homo(heteros[c], oR, 1))
        out = {}
        runs = {}
        for name, hs in (("homo", homos), ("marginal", margs)):
            hm.use(agents, hs)
            runs[name] = text_decisions(agents, cues)
            out[name] = summarize(runs[name], truth)
            print(cond, name, json.dumps(out[name], default=int), flush=True)
        out["homo_contra_marginal"] = diff(runs["homo"], runs["marginal"])
        res[cond] = out
        for p in ("homo", "marginal"):
            for sd in SEEDS:
                specs[f"{cond}|recuerdo_{p}_semilla_{sd}"] = {
                    "heteros": str(tmp / f"{cond}.pkl"), "pesos": p, "semilla": sd}
    for name, r in run_passes(specs).items():
        cond, key = name.split("|")
        res[cond][key] = r
    shutil.rmtree(tmp, ignore_errors=True)
    (hm.OUT / "emparejamiento_desigual.json").write_text(
        json.dumps(res, indent=2, ensure_ascii=False, default=int), encoding="utf-8")
    print(json.dumps(res, indent=2, ensure_ascii=False, default=int))


if __name__ == "__main__":
    main()
