"""
Memoria hetero-asociativa de contenido: el puente label <-> latente.

HeteroAssociativeMemory envuelve a HeteroAssociativeMemory4D (Pineda &
Morales, codigo original en hetero_lib/) con tres ajustes de uso:
  - constructor con la firma (n, m, p, q) del sistema y fold=None
    (los clasificadores MNIST del original no aplican a este dominio),
  - recall por defecto con sampling_n_search, igual que el original,
  - recall_from_left/right aceptan pesos por feature, de modo que las
    memorias homo de cada dominio puedan modular el reconocimiento
    en ambas direcciones (el patron left_eam -> hetero_eam de Pineda
    y su espejo derecho).
"""

import io
import sys
import contextlib
from pathlib import Path

import numpy as np

_HETERO_DIR = Path(__file__).parent / "hetero_lib"
if str(_HETERO_DIR) not in sys.path:
    sys.path.insert(0, str(_HETERO_DIR))

import commons
from hetero_associative_4d import HeteroAssociativeMemory4D


class HeteroAssociativeMemory(HeteroAssociativeMemory4D):
    """HAM 4D entre dominio izquierdo (n, m) y derecho (p, q)."""

    def __init__(self, n: int, m: int, p: int, q: int,
                 iota: float = 0.0, kappa: float = 0.0,
                 xi: int = 0, sigma: float = 0.1):
        es = commons.ExperimentSettings(iota=iota, kappa=kappa, xi=xi, sigma=sigma)
        with contextlib.redirect_stdout(io.StringIO()):
            super().__init__(n=n, p=p, m=m, q=q, es=es, fold=None)

    def update(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return super().update()

    def recognize_from_left(self, cue_a: np.ndarray,
                            left_weights: np.ndarray = None) -> float:
        """Activacion media de la proyeccion del cue izquierdo, modulada
        por los pesos de la memoria homo de ese dominio. Score crudo:
        no aplica gate de containment ni calibracion (eso es decision
        del protocolo que compara agentes)."""
        ca = self.validate(cue_a, 0)
        weights = _norm_weights(left_weights, len(ca))
        projection = self.project(ca, weights, 0)
        total = np.sum(projection)
        count = np.count_nonzero(projection)
        return float(total / count) if count > 0 else 0.0

    def recall_from_left(self, cue_a: np.ndarray, weights=None):
        """label -> latente. Devuelve (r_q, recognized, weight, projection,
        stats) con r_q entero y el sentinel q para dimensiones indefinidas."""
        w = _norm_weights(weights, len(cue_a))
        r_io, recognized, weight, proj, stats = super().recall_from_left(
            cue_a, weights=w)
        r_q = _to_int(r_io, self.q)
        return r_q, bool(recognized), float(weight), proj, stats

    def recall_from_right(self, cue_b: np.ndarray, weights=None):
        """latente -> label. Mismo contrato que recall_from_left."""
        w = _norm_weights(weights, len(cue_b))
        r_io, recognized, weight, proj, stats = super().recall_from_right(
            cue_b, weights=w)
        r_q = _to_int(r_io, self.m)
        return r_q, bool(recognized), float(weight), proj, stats

    def print_stats(self, name: str = ""):
        print(f"[HAM {name}] entropy={self.entropy:.4f}  mean={self.mean:.4f}")


def _norm_weights(weights, n: int) -> np.ndarray:
    """project() es invariante a escala; esto solo evita ceros y NaN."""
    if weights is None:
        return np.ones(n, dtype=float)
    w = np.asarray(weights, dtype=float)
    mx = w.max()
    return (w / mx) if mx > 0 else np.ones(n, dtype=float)


def _to_int(r_io, sentinel: int) -> np.ndarray:
    arr = np.asarray(r_io, dtype=float)
    return np.where(np.isnan(arr), sentinel, arr).astype(np.int32)
