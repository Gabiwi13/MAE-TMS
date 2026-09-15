"""
Sondas de la fase 2 sobre exp9 (modelos v4 en models/).

a) Colapso de primera pista: recall_lived usa la primera pista reconocida de
   la consulta. Cuántas consultas distintas comparten esa primera pista.
b) Por qué la descripción supera al especialista: niveles vivos y entropía
   por coordenada de (i) la lectura inversa del directorio visual (pista nan),
   (ii) la proyección de mem_dom_H condicionada por la etiqueta, (iii) la
   distribución del dominio en mem_dom_R (las 800 instancias del llenado); y
   cuántas instancias distintas quedaron asociadas a cada etiqueta en
   stage5_fill (mem_H.register(label_seq[i % L], z_q[i])).
c) Por qué el especialista no responde en car y horse: para cada consulta
   ruteada a k sin ninguna pista reconocida, qué coordenadas de la etiqueta
   quedan sin soporte en mem_dom_H y si el fallo es de contención.

Escribe results/experimento9/sonda_fase2.json.
"""
import contextlib
import io
import json
import pickle
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
from quantizer import quantize_binary
from stage6_interaction import (CLASSES, AGENT_LIST, MODELS_DIR, M_LABEL, Q_LATENT,
                                get_nlp, load_all_vectors, tokenize_query,
                                get_fasttext_vector, prevectorize)
from stage5_fill import build_label_sequence

K = len(AGENT_LIST)
OUT = ROOT / "results" / "experimento9" / "sonda_fase2.json"


def load_agent(name):
    with open(MODELS_DIR / f"agent_{name}.pkl", "rb") as f:
        return pickle.load(f)


def entropy_bits(P):
    """Entropía media por coordenada (bits) de una matriz (coords x niveles)."""
    s = P.sum(axis=1, keepdims=True)
    live = s[:, 0] > 0
    Q = P[live] / s[live]
    H = -(Q * np.log2(np.where(Q > 0, Q, 1.0))).sum(axis=1)
    return float(H.mean()) if H.size else float("nan")


def live_levels(P):
    return float((P > 0).sum(axis=1).mean())


def label_projection(mem_H, v_q):
    with contextlib.redirect_stdout(io.StringIO()):
        proj = mem_H.project(mem_H.validate(v_q, 0), np.ones(len(v_q)), 0)
    return np.asarray(proj, dtype=float)[:, :Q_LATENT]


def label_support_gaps(mem_H, v_q):
    """Coordenadas de la etiqueta cuyo valor nunca se registró (ningún latente)."""
    rel = mem_H._full_iota_relation
    v = mem_H.validate(v_q, 0).astype(int)
    # :q excluye la columna del valor indefinido, que lleva masa propia
    return [i for i in range(v.size) if rel[i, :, int(v[i]), :mem_H.q].sum() == 0]


def main():
    nlp = get_nlp()
    vectors = load_all_vectors(nlp)
    from eval_bank import ALL_QUERIES, GROUND_TRUTH
    pairs = list(zip(ALL_QUERIES, GROUND_TRUTH))
    toks = set()
    for q, _ in pairs:
        toks.update(tokenize_query(q, nlp))
    prevectorize(vectors, toks, allow_fallback=False)
    bank = []
    for q, t in pairs:
        cues = []
        for tok in tokenize_query(q, nlp):
            v = get_fasttext_vector(tok, vectors, allow_fallback=False)
            if v is not None:
                cues.append((tok, quantize_binary(np.asarray(v, dtype=np.float32), M_LABEL)))
        if cues:
            bank.append({"query": q, "k": AGENT_LIST.index(t), "cues": cues})

    out = {"colapso_primera_pista": {}, "niveles_y_entropia": {}, "emparejamiento_llenado": {},
           "fallos_del_especialista": {}}
    survivor_dir = load_agent(CLASSES[1]).mem_dir      # idéntico entre agentes en v4
    tot_routed = tot_bank = 0
    collapse_routed = Counter()
    for k, cls in enumerate(CLASSES):
        ag = load_agent(cls)
        mem_H = ag.mem_dom_H
        queries = [it for it in bank if it["k"] == k]
        routed = []
        for it in queries:
            with contextlib.redirect_stdout(io.StringIO()):
                dest, _ = survivor_dir.route_multi([v for _, v in it["cues"]], mode="linear")
            if dest == k:
                routed.append(it)

        # a) primera pista reconocida (determinista: proyección sin filas vacías)
        def first_cue(it):
            for tok, v_q in it["cues"]:
                proj = label_projection(mem_H, v_q)
                if np.count_nonzero(proj.sum(axis=1) == 0) == 0:
                    return tok
            return None
        fc_routed = [first_cue(it) for it in routed]
        fc_bank = [first_cue(it) for it in queries]
        cnt_r = Counter(t for t in fc_routed if t is not None)
        cnt_b = Counter(t for t in fc_bank if t is not None)
        out["colapso_primera_pista"][cls] = {
            "ruteadas": len(routed), "responden": sum(t is not None for t in fc_routed),
            "primeras_pistas_distintas_ruteadas": len(cnt_r),
            "consultas_por_pista_ruteadas": dict(cnt_r.most_common()),
            "banco": len(queries), "primeras_pistas_distintas_banco": len(cnt_b),
            "consultas_por_pista_banco": dict(cnt_b.most_common(6)),
        }
        tot_routed += len(routed); tot_bank += len(queries)
        collapse_routed[cls] = sum(n for n in cnt_r.values() if n > 1)

        # b) niveles vivos y entropía
        dir_proj = ag.mem_dir_R.domain_projection(k)                 # pista nan (fix)
        homo_R = np.asarray(ag.mem_dom_R._am._relation, dtype=float)[:, :Q_LATENT]
        cond = {}
        for tok in cnt_r:
            v_q = next(v for it in routed for t, v in it["cues"] if t == tok)
            P = label_projection(mem_H, v_q)
            cond[tok] = {"niveles_vivos": live_levels(P), "entropia_bits": entropy_bits(P)}
        out["niveles_y_entropia"][cls] = {
            "directorio_inverso_nan": {"niveles_vivos": live_levels(dir_proj), "entropia_bits": entropy_bits(dir_proj),
                                       "registros": int(ag.mem_dir_R.agent_counts[k])},
            "mem_dom_H_condicionada_media": {
                "niveles_vivos": float(np.mean([c["niveles_vivos"] for c in cond.values()])) if cond else float("nan"),
                "entropia_bits": float(np.mean([c["entropia_bits"] for c in cond.values()])) if cond else float("nan"),
                "pistas": len(cond)},
            "mem_dom_H_condicionada_por_pista": cond,
            "mem_dom_R_dominio_800": {"niveles_vivos": live_levels(homo_R), "entropia_bits": entropy_bits(homo_R)},
        }

        # b') emparejamiento etiqueta-instancia en el llenado
        seq = build_label_sequence(cls)
        labels = json.loads((ROOT / f"labels_{cls}.json").read_text())
        raw = json.loads((ROOT / f"label_vectors_{cls}.json").read_text())
        words = [w for w, f in labels.items() if w in raw for _ in range(int(f))]
        n_inst = len(json.loads((MODELS_DIR / f"instance_latents_{cls}.json").read_text()))
        L = len(seq)
        per_word = Counter()
        for i in range(n_inst):
            per_word[words[i % L]] += 1
        out["emparejamiento_llenado"][cls] = {
            "instancias": n_inst, "registros_de_etiqueta_L": L, "etiquetas_distintas": len(set(words)),
            "instancias_distintas_por_etiqueta": {"min": min(per_word.values()), "media": float(np.mean(list(per_word.values()))),
                                                  "max": max(per_word.values())},
            "ejemplos": dict(Counter(per_word).most_common(4)),
            "regla": "mem_H.register(label_seq[i % L], z_q[i]): la etiqueta i%L se empareja con la instancia i, sin correspondencia semántica",
        }

        # c) fallos del especialista
        fails = []
        for it, fc in zip(routed, fc_routed):
            if fc is not None:
                continue
            toks = []
            for tok, v_q in it["cues"]:
                gaps = label_support_gaps(mem_H, v_q)
                proj = label_projection(mem_H, v_q)
                empty_rows = int(np.count_nonzero(proj.sum(axis=1) == 0))
                homo_w = ag.mem_dom_L.recog_weights(v_q)
                toks.append({"token": tok, "coordenadas_etiqueta_sin_soporte": gaps,
                             "n_sin_soporte": len(gaps), "filas_latentes_vacias": empty_rows,
                             "homo_L_coords_en_cero": int(np.count_nonzero(homo_w == 0))})
            fails.append({"query": it["query"], "tokens": toks})
        out["fallos_del_especialista"][cls] = {"consultas_sin_respuesta": len(fails), "detalle": fails}
        print(f"{cls:7s} ruteadas {len(routed):2d} responden {sum(t is not None for t in fc_routed):2d} "
              f"pistas distintas {len(cnt_r):2d} top {cnt_r.most_common(2)} | niveles dir {live_levels(dir_proj):.2f} "
              f"H|etiq {out['niveles_y_entropia'][cls]['mem_dom_H_condicionada_media']['niveles_vivos']:.2f} "
              f"R800 {live_levels(homo_R):.2f} | inst/etiqueta {per_word and np.mean(list(per_word.values())):.1f} "
              f"| fallos {len(fails)}", flush=True)
        del ag

    total_collapsed = sum(collapse_routed.values())
    out["colapso_primera_pista"]["total"] = {
        "ruteadas": tot_routed, "consultas_que_comparten_primera_pista_con_otra": total_collapsed,
        "fraccion_ruteadas": total_collapsed / max(tot_routed, 1),
        "primeras_pistas_distintas_ruteadas": sum(v["primeras_pistas_distintas_ruteadas"]
                                                  for c, v in out["colapso_primera_pista"].items() if c != "total"),
    }
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(out["colapso_primera_pista"]["total"], indent=1))
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
