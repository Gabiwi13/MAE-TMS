"""
¿Las memorias homo guardan algo que la hetero no tenga? Con el llenado oficial
cada homo recibe los mismos registros que un lado de la hetero, así que debería
ser su marginal. Se reemplaza cada homo por la marginal de la hetero de su
agente y se repiten, decisión por decisión, las lecturas oficiales. Solo lee
models/; criterio en plan_cierre_pesos_homo.md (29 oct).
"""
import contextlib
import io
import json
import random
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import stage6_interaction as s6
import stage7_bidirectional as s7
from associative_memory import HomoAssociativeMemory
from eval_bank import ALL_QUERIES
from hetero_lib import commons
from hetero_lib.associative import AssociativeMemory
from quantizer import quantize_binary
from stage5_fill import quantize_latent_global

OUT = ROOT / "results" / "homo_marginal"
CLASSES = s6.CLASSES


def marginal_homo(mem_H, like: HomoAssociativeMemory, dim: int):
    rel = np.asarray(mem_H.relation, dtype=np.int64)        # (n, p, m, q)
    marg = rel[:, 0].sum(axis=2) if dim == 0 else rel[0].sum(axis=1)
    return homo_from(marg, like)


def homo_from(table, like: HomoAssociativeMemory):
    """Homo con los parámetros de `like` y la relación `table`."""
    am = like._am
    es = commons.ExperimentSettings(iota=am.iota, kappa=am.kappa, xi=am.xi, sigma=am.sigma)
    h = HomoAssociativeMemory(like.n, like.m, iota=am.iota, kappa=am.kappa, xi=am.xi, sigma=am.sigma)
    with contextlib.redirect_stdout(io.StringIO()):
        h._am = AssociativeMemory.from_relation(table, es)
    return h


def use(agents, homos):
    for c, a in agents.items():
        a.mem_dom_L, a.mem_dom_R = homos[c]
        a.mem_dom_H.attach_homo(*homos[c])


def text_cues(queries, nlp, vectors_cache):
    out = []
    for q in queries:
        cues = []
        for tok in s6.tokenize_query(q, nlp):
            vec = s6.get_fasttext_vector(tok, vectors_cache)
            if vec is not None:
                cues.append(quantize_binary(vec, s6.M_LABEL))
        out.append(cues)
    return out


def measure(agents, queries, cues_by_q, images, all_vecs):
    rows_t, rows_i = [], []
    rng = np.random.RandomState(42)
    for k, (q, cues) in enumerate(zip(queries, cues_by_q)):
        entry = s6.AGENT_LIST[int(rng.randint(len(s6.AGENT_LIST)))]
        scores = [[agents[c].recognize_gated(v) for c in CLASSES] for v in cues]
        tot = np.sum(scores, axis=0) if scores else np.zeros(len(CLASSES))
        early = CLASSES[int(np.argmax(tot))] if tot.sum() > 0 else None
        widx = -1
        gate = False
        if cues:
            widx, *_ = s6.route_transactive(entry, agents, cues, modality="text")
            if widx >= 0:
                gate = max(agents[CLASSES[widx]].recognize_gated(v) for v in cues) > 0
        recalled = None
        if early is not None:
            ti = int(np.argmax([s[CLASSES.index(early)] for s in scores]))
            random.seed(k)
            with contextlib.redirect_stdout(io.StringIO()):
                r_q, ok, *_ = agents[early].mem_dom_H.recall_from_left(cues[ti])
            recalled = r_q.tolist() if ok else None
        rows_t.append({"query": q, "scores": np.asarray(scores).tolist(), "early": early,
                       "mature": None if widx < 0 else CLASSES[widx], "gate": gate,
                       "recall": recalled})
    for k, (cls, ci, z_q) in enumerate(images):
        if z_q is None:
            rows_i.append({"clase": cls, "energia": False})
            continue
        sc = [s7.recognize_gated_right(agents[c], z_q) for c in CLASSES]
        entry = CLASSES[(ci + 1) % len(CLASSES)]
        widx, *_ = s6.route_transactive(entry, agents, z_q, modality="image", xi=s7.XI_VISUAL)
        labels = []
        if widx >= 0:
            random.seed(10_000 + k)
            labels = s7.evoke_labels(agents[CLASSES[widx]], z_q, all_vecs)
        rows_i.append({"clase": cls, "energia": True, "scores": sc,
                       "dest": None if widx < 0 else CLASSES[widx], "labels": labels})
    return rows_t, rows_i


def compare(a, b):
    """Diferencias entre dos corridas, lectura por lectura."""
    t_pairs = cont_t = 0
    rel_t = []
    early = mature = gate = rec_same = rec_n = 0
    rec_dist = []
    for x, y in zip(a[0], b[0]):
        sx, sy = np.asarray(x["scores"]), np.asarray(y["scores"])
        if sx.size:
            t_pairs += sx.size
            cont_t += int(np.count_nonzero((sx > 0) != (sy > 0)))
            m = (sx > 0) & (sy > 0)
            if m.any():
                rel_t.append(float(np.max(np.abs(sx[m] - sy[m]) / sx[m])))
        early += x["early"] != y["early"]
        mature += x["mature"] != y["mature"]
        gate += x["gate"] != y["gate"]
        if x["recall"] is not None and y["recall"] is not None:
            rec_n += 1
            rx, ry = np.asarray(x["recall"]), np.asarray(y["recall"])
            rec_same += int(np.array_equal(rx, ry))
            rec_dist.append(float(np.mean(np.abs(rx - ry))))
    i_n = cont_i = dest = lab = 0
    rel_i = []
    for x, y in zip(a[1], b[1]):
        if not x["energia"]:
            continue
        i_n += 1
        sx, sy = np.asarray(x["scores"]), np.asarray(y["scores"])
        cont_i += int(np.count_nonzero((sx > 0) != (sy > 0)))
        m = (sx > 0) & (sy > 0)
        if m.any():
            rel_i.append(float(np.max(np.abs(sx[m] - sy[m]) / sx[m])))
        dest += x["dest"] != y["dest"]
        lab += x["labels"] != y["labels"]
    return {
        "texto": {"consultas": len(a[0]), "pares_pista_agente": t_pairs,
                  "contencion_distinta": cont_t,
                  "puntaje_dif_relativa_max": max(rel_t) if rel_t else 0.0,
                  "ganador_temprano_distinto": early, "destino_maduro_distinto": mature,
                  "compuerta_distinta": gate, "recuerdos_comparados": rec_n,
                  "recuerdos_identicos": rec_same,
                  "recuerdo_dif_media_por_coordenada": float(np.mean(rec_dist)) if rec_dist else 0.0},
        "imagen": {"imagenes_con_energia": i_n, "contencion_distinta": cont_i,
                   "puntaje_dif_relativa_max": max(rel_i) if rel_i else 0.0,
                   "destino_distinto": dest, "evocacion_top3_distinta": lab},
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()):
        agents = s6.load_agents()
        nlp = s6.get_nlp()
        vectors_cache = s6.load_all_vectors(nlp)
    label_vecs = s6.load_all_vectors()
    all_vecs = {}
    for c in CLASSES:
        all_vecs.update(label_vecs[c])

    official = {c: (a.mem_dom_L, a.mem_dom_R) for c, a in agents.items()}
    marginal = {c: (marginal_homo(a.mem_dom_H, a.mem_dom_L, 0),
                    marginal_homo(a.mem_dom_H, a.mem_dom_R, 1)) for c, a in agents.items()}
    check = {}
    for c in CLASSES:
        (oL, oR), (mL, mR) = official[c], marginal[c]
        rL, rR = np.asarray(oL._am.relation), np.asarray(mL._am.relation)
        sup = rL > 0
        check[c] = {
            "latente_identica": bool(np.array_equal(np.asarray(oR._am.relation),
                                                    np.asarray(mR._am.relation))),
            "etiquetas_mismo_soporte": bool(np.array_equal(sup, rR > 0)),
            "etiquetas_factor_min": float((rR[sup] / rL[sup]).min()),
            "etiquetas_factor_max": float((rR[sup] / rL[sup]).max()),
        }
    print("marginales:", json.dumps(check))

    queries = list(ALL_QUERIES) + list(s6.TEST_QUERIES)
    cues = text_cues(queries, nlp, vectors_cache)

    encoder = s7.load_encoder()
    g_min, g_max = s7.load_global_stats()
    tau = s7.latent_energy_threshold()
    splits = json.loads((s7.DATA_DIR / "splits.json").read_text())
    images = []
    for ci, cls in enumerate(CLASSES):
        for p in splits[cls]["test"]:
            z = s7.image_to_latent(p, encoder)
            zq = quantize_latent_global(z, g_min, g_max, s7.Q_IMG) if s7.latent_has_energy(z, tau) else None
            images.append((cls, ci, zq))
    print(f"{len(queries)} consultas, {len(images)} imagenes")

    use(agents, official)
    run_a = measure(agents, queries, cues, images, all_vecs)
    run_a2 = measure(agents, queries, cues, images, all_vecs)
    use(agents, marginal)
    run_b = measure(agents, queries, cues, images, all_vecs)

    res = {"marginales": check,
           "control_oficial_repetido": compare(run_a, run_a2),
           "oficial_contra_marginal": compare(run_a, run_b)}
    (OUT / "resumen.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "filas.json").write_text(json.dumps({"oficial": run_a, "marginal": run_b},
                                               ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
