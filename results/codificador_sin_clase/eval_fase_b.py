"""Fase B de la etapa 7 en solo lectura: una fila por imagen de test, y la evocación
repetida con semillas fijas (la etapa 7 no fija la de `random`).

Uso: python -B eval_fase_b.py <raíz de la copia> <salida.json> [semillas; 0 = solo ruteo]
"""
import json
import random
import sys
import time
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
sys.path.insert(0, str(root / "src"))

import stage7_bidirectional as s7  # noqa: E402
from stage5_fill import quantize_latent_global  # noqa: E402
from stage6_interaction import CLASSES, load_tme_and_agents, load_all_vectors, route_transactive  # noqa: E402

# Cada evocación tarda ~15 s con la máquina cargada: una pasada (semilla 0) por omisión.
SEEDS = range(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
# Sin el umbral guardado, latent_energy_threshold() lo escribiría; aquí solo se lee.
assert s7.ENERGY_PATH.exists(), f"falta {s7.ENERGY_PATH}"

t0 = time.time()
encoder = s7.load_encoder()
g_min, g_max = s7.load_global_stats()
tau = s7.latent_energy_threshold()
splits = json.loads((s7.DATA_DIR / "splits.json").read_text())
_, agents = load_tme_and_agents()
vecs = load_all_vectors()
vocab = {c: set(vecs[c]) for c in CLASSES}
all_vecs = {}
for c in CLASSES:
    all_vecs.update(vecs[c])

rows, zq = [], {}
for ci, cls in enumerate(CLASSES):
    for j, p in enumerate(splits[cls]["test"]):
        z = s7.image_to_latent(p, encoder)
        r = {"clase": cls, "imagen": Path(p).name, "norma": float(np.linalg.norm(z)), "evoca": False}
        rows.append(r)
        if not s7.latent_has_energy(z, tau):
            r.update(sin_energia=True, destino=None)
            continue
        z_q = quantize_latent_global(z, g_min, g_max, s7.Q_IMG)
        widx, scores, consulted, hops = route_transactive(
            CLASSES[(ci + 1) % len(CLASSES)], agents, z_q, modality="image", xi=s7.XI_VISUAL)
        r.update(sin_energia=False, destino=CLASSES[widx] if widx >= 0 else None,
                 consultados=len(consulted), saltos=hops, puntajes=[float(x) for x in scores],
                 evoca=bool(widx >= 0 and j < s7.N_EVOKE))
        zq[len(rows) - 1] = z_q
    print(f"  ruteo {cls}: {time.time() - t0:.0f} s", flush=True)
t_route = time.time() - t0

evo = [i for i, r in enumerate(rows) if r["evoca"]]
hits = []
for s in SEEDS:
    random.seed(s)
    np.random.seed(s)
    h = 0
    for i in evo:
        r = rows[i]
        labels = s7.evoke_labels(agents[r["destino"]], zq[i], all_vecs)
        hit = any(w in vocab[r["clase"]] for w in labels)
        r.setdefault("evocacion", []).append({"semilla": s, "labels": labels, "hit": hit})
        h += int(hit)
    hits.append(h)
    print(f"  evocación, semilla {s}: {h}/{len(evo)} ({time.time() - t0:.0f} s)", flush=True)

n = len(rows)
ok = sum(r["destino"] == r["clase"] for r in rows)
rej = sum(r["destino"] is None for r in rows)
falsos = [f"{r['clase']} → {r['destino']}" for r in rows if r["destino"] not in (None, r["clase"])]
pares = {}
for k in falsos:
    pares[k] = pares.get(k, 0) + 1
resumen = {
    "raiz": str(root), "tau": tau, "n": n, "ruteo_ok": ok, "ruteo_pct": 100 * ok / n,
    "rechazo": rej, "rechazo_pct": 100 * rej / n, "sin_energia": sum(r["sin_energia"] for r in rows),
    "falsos": len(falsos), "falsos_pares": dict(sorted(pares.items(), key=lambda kv: -kv[1])),
    "por_clase": {c: {"ok": sum(r["destino"] == c for r in rows if r["clase"] == c),
                      "rechazo": sum(r["destino"] is None for r in rows if r["clase"] == c),
                      "n": sum(r["clase"] == c for r in rows)} for c in CLASSES},
    "evocacion": {"denominador": len(evo), "semillas": list(SEEDS), "hits": hits,
                  "media_pct": 100 * float(np.mean(hits)) / max(len(evo), 1) if hits else None},
    "segundos_ruteo": round(t_route), "segundos": round(time.time() - t0),
}
out.write_text(json.dumps({"resumen": resumen, "filas": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(resumen, ensure_ascii=False, indent=1))
