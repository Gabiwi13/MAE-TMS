"""
B. Datos sin pareja: la hetero de cada agente recibe solo una parte de las
imágenes de llenado y la homo latente se queda con todas. ¿La homo reconoce
lo que la hetero no puede nombrar? Las memorias reducidas viven en RAM; no
toca models/. Criterio en plan_cierre_pesos_homo.md (29 oct).
"""
import contextlib
import io
import json
import random
from types import SimpleNamespace

import numpy as np

import run_homo_marginal as hm
from relleno_paralelo import rebuild_heteros
from stage5_fill import build_label_sequence

s6, s7 = hm.s6, hm.s7
CLASSES = hm.CLASSES
VARIANTS = 16
FRACTIONS = (50, 100)        # imágenes emparejadas de las 200 de llenado


def fill_q(c, g_min, g_max):
    raw = json.loads((s6.MODELS_DIR / f"instance_latents_{c}.json").read_text())
    return [hm.quantize_latent_global(np.asarray(z), g_min, g_max, s7.Q_IMG) for z in raw]


def test_images(g_min, g_max):
    encoder = s7.load_encoder()
    tau = s7.latent_energy_threshold()
    splits = json.loads((s7.DATA_DIR / "splits.json").read_text())
    out = []
    for ci, c in enumerate(CLASSES):
        for p in splits[c]["test"]:
            z = s7.image_to_latent(p, encoder)
            if s7.latent_has_energy(z, tau):
                out.append((ci, hm.quantize_latent_global(z, g_min, g_max, s7.Q_IMG)))
    return out


def recognition(homos_R, images):
    own = other = top1 = rejected = 0
    accepted = []
    for ci, z in images:
        sc = np.array([s7.recognize_gated_right(SimpleNamespace(mem_dom_R=homos_R[c]), z)
                       for c in CLASSES])
        acc = sc > 0
        accepted.append(acc)
        own += int(acc[ci])
        other += int(acc.sum() - acc[ci])
        if acc.any():
            top1 += int(int(np.argmax(sc)) == ci)
        else:
            rejected += 1
    n = len(images)
    return {"imagenes": n, "acepta_propia_clase_pct": 100 * own / n,
            "aceptaciones_de_otra_clase": other, "top1_correcto_pct": 100 * top1 / n,
            "rechazadas_por_todos": rejected}, np.array(accepted)


def main():
    hm.OUT.mkdir(parents=True, exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()):
        agents = s6.load_agents()
    g_min, g_max = s7.load_global_stats()
    images = test_images(g_min, g_max)
    official_R = {c: a.mem_dom_R for c, a in agents.items()}
    rec_homo, acc_homo = recognition(official_R, images)
    res = {"homo_oficial_200": rec_homo}
    print("homo oficial", json.dumps(res["homo_oficial_200"]), flush=True)
    for n_img in FRACTIONS:
        jobs = {}
        for c in CLASSES:
            lat = fill_q(c, g_min, g_max)[: n_img * VARIANTS]
            seq = build_label_sequence(c)
            jobs[c] = (agents[c].mem_dom_H, [(seq[i % len(seq)], z) for i, z in enumerate(lat)])
        heteros = rebuild_heteros(jobs)
        marg_R = {}
        for c in CLASSES:
            assert heteros[c].relation.shape == agents[c].mem_dom_H.relation.shape
            marg_R[c] = hm.marginal_homo(heteros[c], agents[c].mem_dom_R, 1)
        rec, acc_marg = recognition(marg_R, images)
        # Imágenes que la homo oficial acepta en su clase y la hetero reducida
        # no puede nombrar: el recuerdo imagen→texto no se reconoce.
        extra = [(i, ci) for i, (ci, _) in enumerate(images)
                 if acc_homo[i, ci] and not acc_marg[i, ci]]
        no_name = 0
        for i, ci in extra:
            z = images[i][1]
            w = official_R[CLASSES[ci]].recog_weights(z)
            random.seed(20_000 + i)
            with contextlib.redirect_stdout(io.StringIO()):
                _, ok, *_ = heteros[CLASSES[ci]].recall_from_right(z, weights=w)
            no_name += int(not ok)
        rec["vistas_extra_de_la_homo"] = len(extra)
        rec["de_ellas_sin_recuerdo_imagen_a_texto"] = no_name
        res[f"marginal_{n_img}_de_200"] = rec
        print(n_img, json.dumps(rec), flush=True)
    (hm.OUT / "sin_pareja.json").write_text(json.dumps(res, indent=2, ensure_ascii=False),
                                            encoding="utf-8")
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
