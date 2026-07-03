"""
Cuantización de pistas semánticas (fastText -> niveles discretos) con escala
global por magnitud, compartida entre llenado y consulta.
"""
import json
from pathlib import Path

import numpy as np

# Escala global para la cuantización por MAGNITUD de las pistas semánticas.
# Antes las etiquetas se binarizaban por signo (solo 2 niveles efectivos), lo que
# no separaba clases solapadas. Ahora se conserva la magnitud de cada componente
# fastText, mapeando [-S, S] -> [0, levels-1] con una escala global S (percentil
# alto de |componente| sobre el vocabulario), consistente entre llenado y consulta.
_SCALE_PATH = Path(__file__).parent.parent / "models" / "label_quant_scale.json"
_LABEL_SCALE = None


def set_label_scale(scale: float) -> None:
    global _LABEL_SCALE
    _LABEL_SCALE = float(scale)


def label_scale() -> float:
    global _LABEL_SCALE
    if _LABEL_SCALE is None:
        try:
            _LABEL_SCALE = float(json.loads(_SCALE_PATH.read_text())["scale"])
        except Exception:
            # Solo puede pasar antes de correr la etapa 4 (que persiste la
            # escala). Avisar: si llenado y consulta usaran escalas distintas,
            # la cuantización dejaría de ser comparable.
            print(f"  ADVERTENCIA: {_SCALE_PATH.name} no disponible; usando "
                  f"escala provisional 0.5. Corre stage4 para la escala real.")
            _LABEL_SCALE = 0.5
    return _LABEL_SCALE




def quantize_binary(vec: np.ndarray, levels: int) -> np.ndarray:
    """Cuantización por MAGNITUD de una pista semántica (fastText 300D en crudo).

    (Se conserva el nombre por compatibilidad con las llamadas existentes, pero
    ya NO es binaria por signo.) Escala global S -> [-1,1] -> [0, levels-1],
    preservando la magnitud de cada componente. La misma S se usa en el llenado
    y en la consulta, así que la cuantización es consistente y comparable.
    """
    s = label_scale()
    v = np.clip(np.asarray(vec, dtype=float) / s, -1.0, 1.0)   # [-1, 1]
    v = (v + 1.0) / 2.0                                         # [0, 1]
    q = np.floor(v * levels).astype(np.int32)
    return np.clip(q, 0, levels - 1)


def compute_label_scale(vectors, pct: float = 99.0) -> float:
    """Escala global = percentil `pct` de |componente| sobre un conjunto de
    vectores (crudos). Robusta a outliers; usa casi todo el rango de niveles."""
    allc = np.abs(np.concatenate([np.asarray(v, dtype=float).ravel()
                                  for v in vectors]))
    s = float(np.percentile(allc, pct))
    return s if s > 1e-6 else 0.5
