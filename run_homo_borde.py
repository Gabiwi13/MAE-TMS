"""
D. ¿La hetero puede guardar lo que llega sin pareja? Se repite B, pero las
imágenes de llenado que quedan sin pareja se registran con la palabra
indefinida (NaN), que la hetero guarda en su borde de funciones parciales.
Se compara con la hetero de B, que solo recibe las emparejadas. Las memorias
viven en RAM; no toca models/. Criterio en plan_cierre_pesos_homo.md (29 oct).
"""
import contextlib
import io
import json
import random

import numpy as np

import run_homo_marginal as hm
from relleno_paralelo import rebuild_heteros
from run_homo_sin_pareja import FRACTIONS, VARIANTS, fill_q, recognition, test_images
from stage5_fill import build_label_sequence

s6, s7 = hm.s6, hm.s7
CLASSES = hm.CLASSES


def border(h):
    """Conteos del borde de palabra indefinida sin el 1 fijo, (n, p, q)."""
    return np.asarray(h._relation[:, :, h.m, :h.q], dtype=np.int64) - 1


def same_state(a, b):
    """Interior de la relación y todo lo que la hetero deriva de él."""
    with contextlib.redirect_stdout(io.StringIO()):
        return {"interior": bool(np.array_equal(a.relation, b.relation)),
                "relacion_iota": bool(np.array_equal(a.iota_relation, b.iota_relation)),
                "medias": bool(np.array_equal(a.means, b.means)),
                "entropias": bool(np.array_equal(a.entropies, b.entropies))}


def main():
    hm.OUT.mkdir(parents=True, exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()):
        agents = s6.load_agents()
    g_min, g_max = s7.load_global_stats()
    images = test_images(g_min, g_max)
    official_R = {c: a.mem_dom_R for c, a in agents.items()}
    rec_homo, acc_homo = recognition(official_R, images)
    res = {"homo_oficial_200": rec_homo}
    print("homo oficial", json.dumps(rec_homo), flush=True)
    for n_img in FRACTIONS:
        jobs = {}
        for c in CLASSES:
            lat = fill_q(c, g_min, g_max)
            seq = build_label_sequence(c)
            k = n_img * VARIANTS
            paired = [(seq[i % len(seq)], z) for i, z in enumerate(lat[:k])]
            no_word = np.full(len(seq[0]), np.nan)
            jobs[f"{c}_borde"] = (agents[c].mem_dom_H, paired + [(no_word, z) for z in lat[k:]])
            jobs[f"{c}_pares"] = (agents[c].mem_dom_H, paired)
        heteros = rebuild_heteros(jobs)

        state, marg_R, border_R = {}, {}, {}
        for c in CLASSES:
            hb, hp = heteros[f"{c}_borde"], heteros[f"{c}_pares"]
            b = border(hb)
            interior = np.asarray(hb.relation, dtype=np.int64)[0].sum(axis=1)
            marg_R[c] = hm.homo_from(interior, official_R[c])
            border_R[c] = hm.homo_from(interior + b[0], official_R[c])
            state[c] = same_state(hb, hp)
            state[c]["borde_igual_en_cada_coordenada_de_palabra"] = bool((b == b[0]).all())
            state[c]["registros_en_el_borde"] = int(b[0].sum() // hb.p)
            state[c]["borde_mas_marginal_igual_a_la_homo_oficial"] = bool(np.array_equal(
                np.asarray(border_R[c]._am.relation), np.asarray(official_R[c]._am.relation)))

        same_proj = 0
        for ci, z in images:
            hb, hp = heteros[f"{CLASSES[ci]}_borde"], heteros[f"{CLASSES[ci]}_pares"]
            w = np.ones(len(z))
            same_proj += int(np.array_equal(hb.project(z, w, 1), hp.project(z, w, 1)))

        rec_marg, acc_marg = recognition(marg_R, images)
        rec_border, acc_border = recognition(border_R, images)
        extra = [(i, ci) for i, (ci, _) in enumerate(images)
                 if acc_homo[i, ci] and not acc_marg[i, ci]]
        no_name = same_recall = 0
        for i, ci in extra:
            z = images[i][1]
            w = official_R[CLASSES[ci]].recog_weights(z)
            out = []
            for key in ("borde", "pares"):
                random.seed(20_000 + i)
                with contextlib.redirect_stdout(io.StringIO()):
                    r, ok, *_ = heteros[f"{CLASSES[ci]}_{key}"].recall_from_right(z, weights=w)
                out.append((np.asarray(r), ok))
            no_name += int(not out[0][1])
            same_recall += int(out[0][1] == out[1][1] and np.array_equal(out[0][0], out[1][0]))

        res[f"{n_img}_de_200"] = {
            "estado_por_agente": state,
            "proyeccion_identica_a_B": f"{same_proj} de {len(images)}",
            "reconocimiento_marginal_del_interior": rec_marg,
            "reconocimiento_borde_mas_marginal": rec_border,
            "decisiones_distintas_borde_contra_homo_oficial": int((acc_border != acc_homo).sum()),
            "vistas_extra_de_la_homo": len(extra),
            "de_ellas_sin_recuerdo_imagen_a_texto": no_name,
            "recuerdo_identico_a_B": f"{same_recall} de {len(extra)}"}
        print(n_img, json.dumps(res[f"{n_img}_de_200"], ensure_ascii=False), flush=True)
        del heteros
    (hm.OUT / "borde.json").write_text(json.dumps(res, indent=2, ensure_ascii=False),
                                       encoding="utf-8")
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
