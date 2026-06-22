"""
Memorias asociativas del sistema: la homo-asociativa de Pineda & Morales
y el directorio transactivo construido sobre la hetero-asociativa.

HomoAssociativeMemory  modela la distribucion de UN dominio; es la unica
                       capaz de producir pesos por feature (recog_weights),
                       que las memorias hetero consumen pero no generan.
DirectoryMemory        directorio de Wegner: registra que agente conoce
                       cada cue y responde "quien sabe esto". Internamente
                       es una HeteroAssociativeMemory4D cuyo dominio derecho
                       es la identidad del agente (one-hot, q=2).
"""

import io
import math
import contextlib
from pathlib import Path
import sys

import numpy as np

_HETERO_DIR = Path(__file__).parent / "hetero_lib"
if str(_HETERO_DIR) not in sys.path:
    sys.path.insert(0, str(_HETERO_DIR))

import commons
from associative import AssociativeMemory
from hetero_associative_4d import HeteroAssociativeMemory4D


class HomoAssociativeMemory:
    """AssociativeMemory de Pineda con salida silenciosa y API estable.

    n features con m niveles de cuantizacion. El constructor del original
    imprime su configuracion; aqui se suprime porque el sistema crea
    decenas de instancias.
    """

    def __init__(self, n: int, m: int,
                 iota: float = 0.0, kappa: float = 0.0,
                 xi: int = 0, sigma: float = 0.1):
        es = commons.ExperimentSettings(iota=iota, kappa=kappa, xi=xi, sigma=sigma)
        with contextlib.redirect_stdout(io.StringIO()):
            self._am = AssociativeMemory(n=n, m=m, es=es)
        self._n = n
        self._m = m

    @property
    def n(self) -> int:
        return self._n

    @property
    def m(self) -> int:
        return self._m

    @property
    def entropy(self) -> float:
        return float(self._am.entropy)

    @property
    def mean(self) -> float:
        return float(self._am.mean)

    def register(self, cue_q: np.ndarray) -> None:
        v = self._am.validate(cue_q)
        r = self._am.to_relation(v)
        self._am.abstract(r)

    def recognize(self, cue_q: np.ndarray) -> float:
        """Peso medio de reconocimiento. Ignora el flag booleano para poder
        comparar agentes incluso ante cues no reconocidos."""
        _, weight = self._am.recognize(cue_q)
        return float(weight)

    def recog_weights(self, cue_q: np.ndarray) -> np.ndarray:
        """Pesos por feature para modular una memoria hetero
        (patron left_eam -> hetero_eam de Pineda). Ceros si el cue
        no fue visto."""
        _, weights = self._am.recog_weights(cue_q)
        return np.asarray(weights, dtype=float)

    def recall(self, cue_q: np.ndarray):
        r_io, recognized, weight = self._am.recall(cue_q)
        return r_io, bool(recognized), float(weight)

    def print_stats(self, name: str = "") -> None:
        print(f"[AM {name}] n={self._n} m={self._m} "
              f"entropy={self.entropy:.4f}  mean={self.mean:.4f}")


class DirectoryMemory:
    """Directorio transactivo (Wegner): asociacion cue -> identidad de agente.

    Soporta las tres operaciones del TMS:
      directory updating      register(cue, agente)
      retrieval coordination  predict / nearest_agent
    La asignacion de informacion (information allocation) ocurre fuera,
    en el protocolo de interaccion que decide al ganador.

    El score crudo de una HAM crece con la masa de registros del agente,
    asi que la lectura para routing se normaliza con predict_normalized
    (B1: ÷count) o se compara via argmax sobre scores ya calibrados.
    """

    def __init__(self, n: int = 300, m: int = 16, n_agents: int = 3,
                 iota: float = 0.0, kappa: float = 0.0,
                 xi: int = 0, sigma: float = 0.1):
        self._n = n
        self._m = m
        self._n_agents = n_agents
        es = commons.ExperimentSettings(iota=iota, kappa=kappa, xi=xi, sigma=sigma)
        with contextlib.redirect_stdout(io.StringIO()):
            self._ham = HeteroAssociativeMemory4D(
                n=n, p=n_agents, m=m, q=2, es=es, fold=None)
        self._counts = np.zeros(n_agents, dtype=np.int64)

    def register(self, v_q: np.ndarray, agent_idx: int) -> None:
        k = int(np.clip(agent_idx, 0, self._n_agents - 1))
        agent_id = np.zeros(self._n_agents, dtype=np.int32)
        agent_id[k] = 1
        self._ham.register(v_q, agent_id)
        self._counts[k] += 1

    def predict(self, v_q: np.ndarray) -> np.ndarray:
        """Score crudo por agente: probabilidad proyectada del bit 'conoce'."""
        weights = np.ones(len(v_q), dtype=float)
        proj = self._ham.project(v_q, weights, dim=0)
        return proj[:, 1].copy()

    def predict_normalized(self, v_q: np.ndarray,
                           mode: str = "linear",
                           eps: float = 1.0) -> np.ndarray:
        """Scores calibrados por masa de registros: linear = ÷(count+eps)."""
        scores = self.predict(v_q)
        denom = self._counts.astype(float) + eps
        return scores / denom if mode == "linear" else scores / np.sqrt(denom)

    def nearest_agent(self, v_q: np.ndarray) -> int:
        """-1 cuando ningun agente tiene señal: el directorio no inventa."""
        scores = self.predict(v_q)
        return -1 if scores.sum() == 0 else int(np.argmax(scores))

    @property
    def agent_counts(self) -> np.ndarray:
        return self._counts.copy()

    def entropy(self) -> float:
        """Entropia de la distribucion de registros entre agentes (bits).
        Maxima = log2(n_agents) cuando la especializacion esta balanceada.

        Un directorio vacio no esta balanceado: esta SIN FORMAR. Devolver
        log2(n_agents) lo haria parecer maximamente organizado desde el
        primer instante (k=0 de la curva de formacion); por eso se reporta
        0.0 bits hasta que haya evidencia registrada."""
        total = float(self._counts.sum())
        if total == 0:
            return 0.0
        p = self._counts / total
        return float(-np.sum(p * np.log2(np.where(p == 0, 1.0, p))))

    def print_stats(self, name: str = "") -> None:
        print(f"[Dir {name}] counts={self._counts.tolist()} "
              f"entropy={self.entropy():.3f} bits")
