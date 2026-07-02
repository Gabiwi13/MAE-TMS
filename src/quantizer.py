"""
Quantizer/dequantizer utilities.
Maps continuous vectors to discrete levels and back.
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
            _LABEL_SCALE = 0.5   # rango típico de fastText si aún no hay stats
    return _LABEL_SCALE


def quantize(vec: np.ndarray, levels: int) -> np.ndarray:
    """
    Map each component of vec to an integer in [0, levels-1].
    Uses uniform quantization over the empirical range.
    """
    vmin, vmax = vec.min(), vec.max()
    if vmax == vmin:
        return np.zeros(len(vec), dtype=np.int32)
    v = (vec - vmin) / (vmax - vmin)  # [0, 1]
    q = np.floor(v * levels).astype(np.int32)
    q = np.clip(q, 0, levels - 1)
    return q


def quantize_batch(matrix: np.ndarray, levels: int) -> np.ndarray:
    """Quantize a 2-D matrix row-wise (each row is one vector)."""
    out = np.zeros_like(matrix, dtype=np.int32)
    for i, row in enumerate(matrix):
        out[i] = quantize(row, levels)
    return out


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


def dequantize(q: np.ndarray, levels: int,
               vmin: float = -1.0, vmax: float = 1.0) -> np.ndarray:
    """Inverse of quantize_binary — maps integers back to floats."""
    v = q.astype(float) / (levels - 1)   # [0, 1]
    return v * (vmax - vmin) + vmin
