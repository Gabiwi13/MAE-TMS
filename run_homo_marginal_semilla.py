"""
Referencia para run_homo_marginal.py, agregada después de ver sus resultados:
¿cuánto cambia el recuerdo texto→latente oficial si solo cambia la semilla?
Así se compara contra los 66 de 420 recuerdos que cambian con la marginal.
"""
import contextlib
import io
import json
import random

import numpy as np

import run_homo_marginal as hm
from eval_bank import ALL_QUERIES

s6 = hm.s6


def recalls(agents, cues_by_q, offset):
    out = []
    for k, cues in enumerate(cues_by_q):
        scores = [[agents[c].recognize_gated(v) for c in hm.CLASSES] for v in cues]
        tot = np.sum(scores, axis=0) if scores else np.zeros(len(hm.CLASSES))
        if not cues or tot.sum() <= 0:
            out.append(None)
            continue
        early = hm.CLASSES[int(np.argmax(tot))]
        ti = int(np.argmax([s[hm.CLASSES.index(early)] for s in scores]))
        random.seed(offset + k)
        with contextlib.redirect_stdout(io.StringIO()):
            r_q, ok, *_ = agents[early].mem_dom_H.recall_from_left(cues[ti])
        out.append(r_q if ok else None)
    return out


def diff(a, b):
    n = same = 0
    dist = []
    for x, y in zip(a, b):
        if x is None or y is None:
            continue
        n += 1
        same += int(np.array_equal(x, y))
        dist.append(float(np.mean(np.abs(x - y))))
    return {"recuerdos_comparados": n, "recuerdos_identicos": same,
            "recuerdo_dif_media_por_coordenada": float(np.mean(dist))}


def main():
    with contextlib.redirect_stdout(io.StringIO()):
        agents = s6.load_agents()
        nlp = s6.get_nlp()
        vectors_cache = s6.load_all_vectors(nlp)
    queries = list(ALL_QUERIES) + list(s6.TEST_QUERIES)
    cues = hm.text_cues(queries, nlp, vectors_cache)
    official = recalls(agents, cues, 0)
    res = {"oficial_semilla_k_contra_k+100000": diff(official, recalls(agents, cues, 100_000))}
    marginal = {c: (hm.marginal_homo(a.mem_dom_H, a.mem_dom_L, 0),
                    hm.marginal_homo(a.mem_dom_H, a.mem_dom_R, 1)) for c, a in agents.items()}
    hm.use(agents, marginal)
    res["oficial_contra_marginal_misma_semilla"] = diff(official, recalls(agents, cues, 0))
    (hm.OUT / "semilla.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
