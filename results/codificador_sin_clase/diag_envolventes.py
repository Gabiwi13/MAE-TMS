"""Diagnóstico añadido después de ver el ruteo (solo lectura): cuántas memorias de contenido
contienen cada imagen de test, y qué tan separadas están las clases coordenada por coordenada.

Uso: python -B diag_envolventes.py <raíz de la copia> <salida.json>
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
sys.path.insert(0, str(root / "src"))

import stage7_bidirectional as s7  # noqa: E402
from stage5_fill import quantize_latent_global, FILL_VARIANTS  # noqa: E402
from stage6_interaction import CLASSES, load_tme_and_agents  # noqa: E402

assert s7.ENERGY_PATH.exists()
encoder = s7.load_encoder()
g_min, g_max = s7.load_global_stats()
tau = s7.latent_energy_threshold()
splits = json.loads((s7.DATA_DIR / "splits.json").read_text())
_, agents = load_tme_and_agents()

# Contención por la memoria de contenido de cada agente (score visual puro de la fase A).
acepta = {c: [] for c in CLASSES}
for cls in CLASSES:
    for p in splits[cls]["test"]:
        z = s7.image_to_latent(p, encoder)
        if not s7.latent_has_energy(z, tau):
            continue
        z_q = quantize_latent_global(z, g_min, g_max, s7.Q_IMG)
        acepta[cls].append([s7.recognize_gated_right(agents[c], z_q) > 0 for c in CLASSES])
por_clase = {}
for cls in CLASSES:
    a = np.array(acepta[cls])
    ci = CLASSES.index(cls)
    por_clase[cls] = {"n": len(a), "propia_acepta": float(a[:, ci].mean()),
                      "ajenas_que_aceptan_media": float((a.sum(1) - a[:, ci]).mean()),
                      "alguna_ajena_acepta": float(((a.sum(1) - a[:, ci]) > 0).mean())}
todas = np.concatenate([np.array(acepta[c]) for c in CLASSES])
propia = np.concatenate([np.array(acepta[c])[:, CLASSES.index(c)] for c in CLASSES])

# Separación por coordenada sobre los originales del llenado: varianza entre medias de clase
# sobre la varianza media dentro de clase.
Z = {c: np.asarray(json.loads((s7.MODELS_DIR / f"instance_latents_{c}.json").read_text()),
                   dtype=np.float32)[::FILL_VARIANTS] for c in CLASSES}
medias = np.stack([Z[c].mean(0) for c in CLASSES])
dentro = np.stack([Z[c].var(0) for c in CLASSES]).mean(0)
fisher = medias.var(0) / dentro
# Ancho de la envolvente cuantizada: niveles distintos que ocupa cada clase por coordenada.
Zq = {c: np.stack([quantize_latent_global(z, g_min, g_max, s7.Q_IMG) for z in Z[c]]) for c in CLASSES}
niveles = {c: float(np.mean([len(np.unique(Zq[c][:, d])) for d in range(Zq[c].shape[1])])) for c in CLASSES}

res = {"raiz": str(root), "n_test_con_energia": int(len(todas)),
       "propia_acepta": float(propia.mean()),
       "ajenas_que_aceptan_media": float((todas.sum(1) - propia).mean()),
       "alguna_ajena_acepta": float(((todas.sum(1) - propia) > 0).mean()),
       "por_clase": por_clase,
       "fisher_por_coordenada": {"mediana": float(np.median(fisher)), "media": float(fisher.mean()),
                                 "max": float(fisher.max()), "n_mayor_que_1": int((fisher > 1).sum())},
       "niveles_ocupados_por_coordenada": niveles}
out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=1))
