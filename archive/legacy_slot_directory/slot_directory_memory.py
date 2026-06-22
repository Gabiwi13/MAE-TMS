"""
LEGACY — NO USAR EN RESULTADOS FINALES.

SlotDirectoryMemory: directorio aproximado del ablation original, una
HomoAssociativeMemory independiente por agente. El sistema oficial usa
DirectoryMemory (hetero, associative_memory.py): una HeteroAssociativeMemory4D
cuyo dominio derecho es la identidad del agente.

Por que se archiva: el score homo crece con la masa de registros mucho mas
rapido que la proyeccion hetero, asi que SlotDirectoryMemory EXAGERA el sesgo
de densidad (la condicion A del ablation caia ~33% y B1 lo "arreglaba" a ~98%).
Con el directorio hetero real el gap es mucho menor (~84% -> ~97%). Citar los
numeros de SlotDirectoryMemory como propiedades del sistema final es incorrecto.

Se conserva solo como referencia historica. No importar desde codigo oficial.
"""

import math

import numpy as np

# Dependía de HomoAssociativeMemory (src/associative_memory.py). Para usarlo de
# forma histórica habría que añadir src/ al sys.path e importarlo explícitamente.
from associative_memory import HomoAssociativeMemory


class SlotDirectoryMemory:
    """Directorio legado del ablation: una HomoAssociativeMemory por agente."""

    def __init__(self, n: int = 300, m: int = 16, n_agents: int = 3,
                 iota: float = 0.0, kappa: float = 0.0,
                 xi: int = 0, sigma: float = 0.1):
        self._n = n
        self._m = m
        self._n_agents = n_agents
        kw = dict(iota=iota, kappa=kappa, xi=xi, sigma=sigma)
        self._ams = [HomoAssociativeMemory(n, m, **kw)
                     for _ in range(n_agents)]
        self._counts = np.zeros(n_agents, dtype=np.int64)

    def register(self, v_q: np.ndarray, agent_idx: int) -> None:
        k = int(np.clip(agent_idx, 0, self._n_agents - 1))
        self._ams[k].register(v_q)
        self._counts[k] += 1

    def predict(self, v_q: np.ndarray) -> np.ndarray:
        return np.array([am.recognize(v_q) for am in self._ams], dtype=float)

    def predict_normalized(self, v_q: np.ndarray, mode: str = "linear",
                           eps: float = 1.0) -> np.ndarray:
        scores = self.predict(v_q)
        denom = self._counts.astype(float) + eps
        return scores / denom if mode == "linear" else scores / np.sqrt(denom)

    def nearest_agent(self, v_q: np.ndarray) -> int:
        scores = self.predict(v_q)
        return -1 if scores.sum() == 0 else int(np.argmax(scores))

    @property
    def agent_counts(self) -> np.ndarray:
        return self._counts.copy()

    def entropy(self) -> float:
        total = float(self._counts.sum())
        if total == 0:
            return math.log2(max(self._n_agents, 1))
        p = self._counts / total
        return float(-np.sum(p * np.log2(np.where(p == 0, 1.0, p))))


class DirectoryMemoryBalanced(SlotDirectoryMemory):
    """Variante con cap proporcional de registros por agente (condición C)."""

    def __init__(self, n=300, m=16, n_agents=3, max_ratio=3.0):
        super().__init__(n=n, m=m, n_agents=n_agents)
        self._max_ratio = max_ratio

    def register(self, v_label_q: np.ndarray, agent_idx: int):
        min_c = self._counts.min()
        if min_c > 0 and self._counts[agent_idx] > min_c * self._max_ratio:
            return  # Skip: agente demasiado dominante
        super().register(v_label_q, agent_idx)
