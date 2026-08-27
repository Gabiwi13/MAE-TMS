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
        # Pasar SIEMPRE los 4 parametros: ExperimentSettings escribe sobre
        # commons.params_defaults (lista global compartida, bug upstream);
        # una construccion parcial heredaria valores del ultimo barrido.
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

    def __init__(self, n: int = 300, m: int = 16, n_agents: int = None,
                 iota: float = 0.0, kappa: float = 0.0,
                 xi: int = 0, sigma: float = 0.1):
        # n_agents es obligatorio: un default construiría un directorio del
        # tamaño equivocado sin fallar.
        if n_agents is None:
            raise TypeError("DirectoryMemory requiere n_agents explícito "
                            "(número de agentes del sistema).")
        self._n = n
        self._m = m
        self._n_agents = n_agents
        # Mismo aviso que en HomoAssociativeMemory: pasar los 4 parametros
        # (ExperimentSettings muta commons.params_defaults).
        es = commons.ExperimentSettings(iota=iota, kappa=kappa, xi=xi, sigma=sigma)
        with contextlib.redirect_stdout(io.StringIO()):
            self._ham = HeteroAssociativeMemory4D(
                n=n, p=n_agents, m=m, q=2, es=es, fold=None)
        self._counts = np.zeros(n_agents, dtype=np.int64)

    def register(self, v_q: np.ndarray, agent_idx: int) -> None:
        # Un indice fuera de rango viene de confundir indice de clase con
        # indice de agente. Se lanza en vez de recortar, porque recortar lo
        # guardaria en el agente equivocado.
        k = int(agent_idx)
        if not 0 <= k < self._n_agents:
            raise ValueError(
                f"agent_idx={agent_idx} fuera de rango [0, {self._n_agents}).")
        agent_id = np.zeros(self._n_agents, dtype=np.int32)
        agent_id[k] = 1
        self._ham.register(v_q, agent_id)
        self._counts[k] += 1

    def predict(self, v_q: np.ndarray) -> np.ndarray:
        """Score crudo por agente: probabilidad proyectada del bit 'conoce'."""
        weights = np.ones(len(v_q), dtype=float)
        proj = self._ham.project(v_q, weights, dim=0)
        return proj[:, 1].copy()

    def _calibrated(self, scores: np.ndarray, mode: str,
                    eps: float) -> np.ndarray:
        """Divide los scores por el numero de registros de cada agente.
        Un mode desconocido lanza en vez de caer a un default."""
        denom = self._counts.astype(float) + eps
        if mode == "linear":
            return scores / denom
        if mode == "sqrt":
            return scores / np.sqrt(denom)
        raise ValueError(f"mode desconocido: {mode!r} (usa 'linear' o 'sqrt')")

    def predict_normalized(self, v_q: np.ndarray,
                           mode: str = "linear",
                           eps: float = 1.0) -> np.ndarray:
        """Scores calibrados por masa de registros: linear = ÷(count+eps)."""
        return self._calibrated(self.predict(v_q), mode, eps)

    def nearest_agent(self, v_q: np.ndarray) -> int:
        """Indice del agente con mayor score crudo, o -1 si ninguno tiene señal."""
        scores = self.predict(v_q)
        return -1 if scores.sum() == 0 else int(np.argmax(scores))

    def support_gaps(self, v_q: np.ndarray) -> list:
        """Coordenadas de la pista sin soporte en la relacion: ese valor nunca
        se registro para ningun agente. Equivale al recog_weights de la homo
        (w_i = R[i, a_i]) sobre el dominio izquierdo del tensor 4D."""
        ham = self._ham
        v = ham.validate(np.asarray(v_q, dtype=float), 0).astype(int)
        rel = ham._full_iota_relation
        return [i for i in range(v.size)
                if not ham.is_undefined(int(v[i]), 0)
                and rel[i, :, int(v[i]), :ham.q].sum() == 0]

    def predict_tolerant(self, v_q: np.ndarray, xi: int = 0,
                         mode: str = "linear", eps: float = 1.0) -> np.ndarray:
        """Hasta xi coordenadas sin soporte se marcan como 'undefined' y la
        proyeccion las salta; el resto de la pista decide. Con mas de xi
        huecos devuelve scores en cero. xi=0 es la lectura estricta."""
        gaps = self.support_gaps(v_q)
        if len(gaps) > xi:
            return np.zeros(self._n_agents, dtype=float)
        if gaps:
            v = self._ham.validate(np.asarray(v_q, dtype=float), 0).astype(int)
            v[gaps] = self._ham.undefined(0)
            weights = np.ones(len(v), dtype=float)
            with contextlib.redirect_stdout(io.StringIO()):
                proj = self._ham.project(v, weights, dim=0)
            scores = proj[:, 1].copy()
        else:
            scores = self.predict(v_q)
        return self._calibrated(scores, mode, eps)

    def route(self, v_q: np.ndarray, mode: str = "linear",
              eps: float = 1.0, xi: int = 0) -> int:
        """Indice del agente ganador, o -1 si ninguno tiene soporte. Calibra
        por masa de registros antes del argmax; xi>0 usa la lectura tolerante."""
        scores = (self.predict_tolerant(v_q, xi=xi, mode=mode, eps=eps)
                  if xi > 0 else self.predict_normalized(v_q, mode=mode, eps=eps))
        # En empate exacto np.argmax devuelve el indice menor.
        return -1 if scores.sum() == 0 else int(np.argmax(scores))

    def route_multi(self, cues, mode: str = "linear",
                    eps: float = 1.0, xi: int = 0):
        """Rutea con varias pistas a la vez (una por token): suma los scores
        calibrados de cada pista y saca el argmax dentro de la memoria.

        Devuelve (winner_idx, scores_sumados); winner_idx = -1 si ninguna
        pista tiene soporte."""
        total = np.zeros(self._n_agents, dtype=float)
        for v_q in cues:
            total += (self.predict_tolerant(v_q, xi=xi, mode=mode, eps=eps)
                      if xi > 0
                      else self.predict_normalized(v_q, mode=mode, eps=eps))
        winner = -1 if total.sum() == 0 else int(np.argmax(total))
        return winner, total

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
