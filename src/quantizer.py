"""
Cuantización de pistas semánticas (fastText -> niveles discretos) con escala
global por magnitud, compartida entre llenado y consulta.
"""
import json
from pathlib import Path

import numpy as np

# Escala global para cuantizar las pistas semánticas por magnitud: cada
# componente fastText pasa de [-S, S] a [0, levels-1], con S = percentil 99 de
# |componente| sobre el vocabulario. La EAM solo acepta valores discretos
# (n características × m niveles), así que este es el paso de entrada.
#
# Por qué p99 y no el máximo: con el máximo (0.579) casi todo se concentra en
# pocos niveles (1.95 de 4 bits); con p99 se usan los 16 niveles (3.46 bits) y
# se recorta el 1% de las componentes. Por signo solo quedan 2 niveles y las
# clases parecidas no se separan. Sin escala, los valores caen en [-0.41, 0.58]
# y los 159 labels van todos al bin 0.
#
# S es global y se guarda en disco porque la misma palabra tiene que cuantizar
# igual al llenar y al consultar; si no, la memoria no la reconoce.
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
        except FileNotFoundError:
            # Una escala de relleno cuantizaria distinto que la real y el
            # llenado dejaria de coincidir con la consulta. Un archivo
            # corrupto tampoco se captura aqui: debe propagarse igual.
            raise FileNotFoundError(
                f"{_SCALE_PATH} no existe. La escala global de cuantizacion "
                f"se genera en Etapa 4 (src/stage4_fasttext.py, funcion "
                f"run()) junto con label_vectors_*.json. Corre "
                f"'python src/stage4_fasttext.py' antes de usar quantize_binary "
                f"o label_scale().")
    return _LABEL_SCALE


def quantize_binary(vec: np.ndarray, levels: int) -> np.ndarray:
    """Cuantiza una pista semántica (fastText 300D en crudo) por magnitud.

    A pesar del nombre, no binariza por signo: divide entre la S global para
    caer en [-1, 1] y mapea a [0, levels-1], conservando la magnitud de cada
    componente. Usa la misma S en el llenado y en la consulta.
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
