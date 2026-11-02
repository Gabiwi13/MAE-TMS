"""Líneas base de imagen sin memoria asociativa sobre los latentes del
codificador oficial. Diseño en README.md.

Uso:  python results/lineas_base/lineas_base_imagen.py
"""
import contextlib
import io
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import torch

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stage5_fill import quantize_latent_global, FILL_VARIANTS
from stage6_interaction import CLASSES, DEVICE, MODELS_DIR, load_tme_and_agents, route_transactive
from stage7_bidirectional import (
    load_encoder, image_to_latent, load_global_stats, latent_energy_threshold,
    latent_has_energy, XI_VISUAL, Q_IMG,
)
import stage2_encoder as s2

K = len(CLASSES)
TOL = 1e-9


def local_path(p):
    parts = Path(p.replace("\\", "/")).parts
    return ROOT / "data" / "eth80" / parts[-2] / parts[-1]


def dequant(q, g_min, g_max, levels=Q_IMG):
    return g_min + (np.asarray(q, dtype=np.float64) + 0.5) / levels * (g_max - g_min)


def top_set(s, higher=True):
    s = np.asarray(s, dtype=np.float64)
    m = s.max() if higher else s.min()
    return [i for i in range(K) if abs(s[i] - m) <= TOL * max(1.0, abs(m))]


def unit(X):
    return X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)


def sims(Z, F, metric):
    """Similitud (mayor = más cerca): -distancia euclidiana o coseno."""
    if metric == "cos":
        return unit(Z) @ unit(F).T
    d2 = (Z ** 2).sum(1)[:, None] + (F ** 2).sum(1)[None, :] - 2 * Z @ F.T
    return -np.sqrt(np.maximum(d2, 0))


def knn_decide(row, fcls, k):
    order = np.argsort(-row, kind="stable")
    kth = row[order[k - 1]]
    take = np.where(row >= kth - TOL * max(1.0, abs(kth)))[0]
    votes = np.bincount(fcls[take], minlength=K).astype(float)
    top = top_set(votes)
    if len(top) > 1:
        mean_sim = np.array([row[take][fcls[take] == c].mean() if c in top else -np.inf
                             for c in range(K)])
        top = top_set(mean_sim)
    return top


def evaluate(Z, F, fcls, truth):
    out = {}
    for metric in ("euc", "cos"):
        cents = np.stack([F[fcls == c].mean(0) for c in range(K)])
        S = sims(Z, cents, metric)
        out[f"centroide_{metric}"] = [top_set(r) for r in S]
        S = sims(Z, F, metric)
        out[f"1nn_{metric}"] = [knn_decide(r, fcls, 1) for r in S]
        out[f"5nn_{metric}"] = [knn_decide(r, fcls, 5) for r in S]
    res = {}
    for name, tops in out.items():
        exp = sum((1.0 / len(t)) if y in t else 0.0 for t, y in zip(tops, truth))
        inf = [int(len(t) == 1 and t[0] == y) for t, y in zip(tops, truth)]
        res[name] = {"tops": tops, "esperado": exp, "inf": inf,
                     "empates": sum(len(t) > 1 for t in tops),
                     "falsos_sin_empate": sum(len(t) == 1 and t[0] != y for t, y in zip(tops, truth))}
    return res


def mcnemar(a, b):
    n01 = sum(1 for x, y in zip(a, b) if x == 0 and y == 1)
    n10 = sum(1 for x, y in zip(a, b) if x == 1 and y == 0)
    n = n01 + n10
    if n == 0:
        return n10, n01, 1.0
    p = sum(math.comb(n, i) for i in range(min(n01, n10) + 1)) / 2 ** n
    return n10, n01, min(1.0, 2 * p)


def main():
    t0 = time.time()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    assert list(s2.CLASSES) == list(CLASSES)
    splits = json.loads((ROOT / "data" / "eth80" / "splits.json").read_text())
    g_min, g_max = load_global_stats()
    tau = latent_energy_threshold()
    encoder = load_encoder()

    paths, truth = [], []
    for ci, c in enumerate(CLASSES):
        for p in splits[c]["test"]:
            paths.append(local_path(p)); truth.append(ci)
    assert all(p.exists() for p in paths)
    Z = np.stack([image_to_latent(str(p), encoder) for p in paths]).astype(np.float64)
    print(f"{len(paths)} latentes de prueba ({time.time()-t0:.1f}s)", flush=True)

    # sistema: fase B de la etapa 7 con los directorios oficiales
    _tme, agents = load_tme_and_agents()
    sys_dest, n_deg = [], 0
    for i, (p, ci) in enumerate(zip(paths, truth)):
        z = Z[i].astype(np.float32)
        if not latent_has_energy(z, tau):
            sys_dest.append(-2); n_deg += 1
            continue
        z_q = quantize_latent_global(Z[i], g_min, g_max, Q_IMG)
        entry = CLASSES[(ci + 1) % K]
        with contextlib.redirect_stdout(io.StringIO()):
            widx, *_ = route_transactive(entry, agents, z_q, modality="image", xi=XI_VISUAL)
        sys_dest.append(widx)
    sys_ok = [int(d == y) for d, y in zip(sys_dest, truth)]
    sys_false = sum(1 for d, y in zip(sys_dest, truth) if d >= 0 and d != y)
    sys_rej = sum(1 for d in sys_dest if d < 0)
    print(f"Sistema: {sum(sys_ok)}/{len(truth)} aciertos, {sys_false} falsos, "
          f"{sys_rej} rechazos ({n_deg} sin energía)", flush=True)

    # cabeza de clasificación del codificador
    clf = s2.Classifier().to(DEVICE)
    clf.load_state_dict(torch.load(MODELS_DIR / "classifier.pt", map_location=DEVICE))
    clf.eval()
    with torch.no_grad():
        logits = clf(torch.tensor(Z, dtype=torch.float32, device=DEVICE)).cpu().numpy()
    clf_pred = logits.argmax(1)
    clf_ok = [int(p == y) for p, y in zip(clf_pred, truth)]

    # llenado
    fill = {}
    for ci, c in enumerate(CLASSES):
        fill[c] = np.asarray(json.loads((MODELS_DIR / f"instance_latents_{c}.json").read_text()),
                             dtype=np.float64)
    sets = {}
    for name, sl in (("16var", slice(None)), ("var0", slice(None, None, FILL_VARIANTS))):
        F = np.concatenate([fill[c][sl] for c in CLASSES])
        fcls = np.concatenate([np.full(len(fill[c][sl]), ci) for ci, c in enumerate(CLASSES)])
        sets[name] = (F, fcls)
    print("Llenado: " + ", ".join(f"{k} {len(v[0])}" for k, v in sets.items()), flush=True)

    reps = {"crudo": (Z, lambda F: F)}
    Zq = np.stack([dequant(quantize_latent_global(z, g_min, g_max, Q_IMG), g_min, g_max) for z in Z])
    reps["cuant"] = (Zq, lambda F: np.stack([dequant(quantize_latent_global(f, g_min, g_max, Q_IMG),
                                                     g_min, g_max) for f in F]))

    table, rows = [], []
    n = len(truth)
    table.append({"decisor": "sistema (route_transactive, etapa 7)", "acierto": sum(sys_ok),
                  "pct": round(100 * sum(sys_ok) / n, 2), "falsos": sys_false, "rechazos": sys_rej,
                  "sin_energia": n_deg})
    table.append({"decisor": "clasificador del codificador (extra)", "acierto": sum(clf_ok),
                  "pct": round(100 * sum(clf_ok) / n, 2), "falsos": n - sum(clf_ok), "rechazos": 0,
                  "mcnemar_vs_sistema (solo_x, solo_sistema, p)": mcnemar(clf_ok, sys_ok)})
    for rep, (Zr, fmap) in reps.items():
        for fname, (F, fcls) in sets.items():
            t1 = time.time()
            res = evaluate(Zr, fmap(F), fcls, truth)
            for dname, r in res.items():
                table.append({"decisor": f"{dname}|{fname}|{rep}",
                              "acierto": round(r["esperado"], 2),
                              "pct": round(100 * r["esperado"] / n, 2),
                              "falsos": round(n - r["esperado"], 2), "rechazos": 0,
                              "empates": r["empates"],
                              "falsos_sin_empate": r["falsos_sin_empate"],
                              "mcnemar_vs_sistema (solo_x, solo_sistema, p)": mcnemar(r["inf"], sys_ok)})
                for i, (t, y) in enumerate(zip(r["tops"], truth)):
                    rows.append({"decisor": f"{dname}|{fname}|{rep}", "imagen": paths[i].name,
                                 "truth": CLASSES[y], "pred": [CLASSES[j] for j in t]})
            print(f"  {rep} {fname}: {time.time()-t1:.1f}s", flush=True)
    for i, p in enumerate(paths):
        rows.append({"decisor": "sistema", "imagen": p.name, "truth": CLASSES[truth[i]],
                     "pred": [CLASSES[sys_dest[i]]] if sys_dest[i] >= 0 else ["REJ"]})
        rows.append({"decisor": "clasificador", "imagen": p.name, "truth": CLASSES[truth[i]],
                     "pred": [CLASSES[int(clf_pred[i])]]})

    secs = round(time.time() - t0, 1)
    (OUT / "resumen_imagen.json").write_text(json.dumps(
        {"tabla": table, "n": n, "tau_energia": tau, "dispositivo": str(DEVICE), "segundos": secs},
        ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    (OUT / "filas_imagen.json").write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    for r in table:
        print(r)
    print(f"Tiempo total {secs}s")


if __name__ == "__main__":
    main()
