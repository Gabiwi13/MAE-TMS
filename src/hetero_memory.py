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

# Métodos de recuperación del paper de la pista faltante (morales2025missing):
#   "random"        Random Samples (RS): una muestra del plano proyectado,
#                   sin prueba de aceptación.
#   "sample_test"   Sample-and-Test (ST): sample_size muestras; gana la de
#                   menor distancia retro-proyectada a la pista (el "test").
#   "sample_search" Sample-and-Search (SS): ST + descenso local por vecindad.
#                   Es el recall original de Pineda & Morales y el default
#                   histórico de este sistema.
MISSING_CUE_METHODS = ("random", "sample_test", "sample_search")


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

    def recall_from_left(self, cue_a: np.ndarray, weights=None,
                         method: str = "sample_search"):
        """label -> latente. Devuelve (r_q, recognized, weight, projection,
        stats) con r_q entero y el sentinel q para dimensiones indefinidas.
        `method` selecciona la variante de recuperación (MISSING_CUE_METHODS)."""
        w = _norm_weights(weights, len(cue_a))
        if method == "sample_search":
            r_io, recognized, weight, proj, stats = super().recall_from_left(
                cue_a, weights=w)
        else:
            r_io, recognized, weight, proj, stats = self._recall_variant(
                cue_a, w, 0, method)
        r_q = _to_int(r_io, self.q)
        return r_q, bool(recognized), float(weight), proj, stats

    def recall_from_right(self, cue_b: np.ndarray, weights=None,
                          method: str = "sample_search"):
        """latente -> label. Mismo contrato que recall_from_left."""
        w = _norm_weights(weights, len(cue_b))
        if method == "sample_search":
            r_io, recognized, weight, proj, stats = super().recall_from_right(
                cue_b, weights=w)
        else:
            r_io, recognized, weight, proj, stats = self._recall_variant(
                cue_b, w, 1, method)
        r_q = _to_int(r_io, self.m)
        return r_q, bool(recognized), float(weight), proj, stats

    def _recall_variant(self, cue: np.ndarray, weights: np.ndarray,
                        dim: int, method: str):
        """RS y ST del paper de la pista faltante, sobre la misma proyección
        AND-ponderada que usa el recall oficial. El "test" de ST es el mismo
        de sample_n_search_recall: retro-proyectar el candidato al dominio de
        la pista y medir distance_recall contra la pista original."""
        if method not in ("random", "sample_test"):
            raise ValueError(f"Método desconocido: {method}")
        cue = self.validate(cue, dim)
        projection = self.project(cue, weights, dim)
        if np.count_nonzero(np.sum(projection, axis=1) == 0) > 0:
            r_io = self.undefined_function(self.alt(dim))
            return r_io, False, 0.0, projection, [0, float("nan")]
        r_io, ws = self.reduce(projection, self.alt(dim))
        distance = self.distance_recall(cue, weights, r_io, ws, dim)
        tested = 1
        if method == "sample_test":
            for _ in range(commons.sample_size - 1):
                q_io, q_ws = self.reduce(projection, self.alt(dim))
                d = self.distance_recall(cue, weights, q_io, q_ws, dim)
                tested += 1
                if d < distance:
                    r_io, ws, distance = q_io, q_ws, d
        weight = float(np.mean(ws)) if len(ws) else 0.0
        r_io = self.revalidate(r_io, self.alt(dim))
        return r_io, True, weight, projection, [tested, float(distance)]

    def prototype_from_left(self, cue_a: np.ndarray, weights=None):
        """Lectura determinista del plano proyectado: el valor más probable
        por columna (argmax). Es el prototipo emergente de la masa
        indeterminada — no pasa por muestreo ni por prueba de aceptación.
        Devuelve (proto_q, projection); proto_q es None si la pista no está
        contenida (alguna columna sin soporte)."""
        w = _norm_weights(weights, len(cue_a))
        ca = self.validate(cue_a, 0)
        projection = self.project(ca, w, 0)
        if np.count_nonzero(np.sum(projection, axis=1) == 0) > 0:
            return None, projection
        proto_q = np.argmax(projection, axis=1).astype(np.int32)
        return proto_q, projection

    def backward_distance_from_left(self, cue_a: np.ndarray,
                                    r_q: np.ndarray, weights=None) -> float:
        """El "test" del paper aplicado a un patrón ya recuperado:
        retro-proyectarlo al dominio de la pista y medir la distancia
        ponderada contra la pista original. Métrica común para comparar
        los tres métodos y el prototipo."""
        w = _norm_weights(weights, len(cue_a))
        ca = self.validate(cue_a, 0)
        projection = self.project(ca, w, 0)
        q_io = self.validate(np.asarray(r_q, dtype=float), 1)
        q_ws = self.weights_in_projection(projection, q_io, 1)
        return float(self.distance_recall(ca, w, q_io, q_ws, 0))

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
