"""
PinedaAssociativeMemory — wrapper around AssociativeMemory from Pineda & Morales.
PinedaDirectoryMemory  — M_dir routing using n_agents AssociativeMemory instances.

Architecture:
  Each Agent has 4 AMRs:
    mem_dom_L  AssociativeMemory(n=300, m=16)         homo-associative label domain
    mem_dom_R  AssociativeMemory(n=64,  m=32)         homo-associative latent domain
    mem_dom_H  PinedaHAM4D(300, 16, 64, 32)           hetero-associative label↔latent
    mem_dir    PinedaDirectoryMemory(n=300, m=16)      routing label→agent

  TME has 2 AMRs:
    mem_dir_L  PinedaDirectoryMemory(n=300, m=16)     label→agent routing
    mem_dir_R  PinedaDirectoryMemory(n=64,  m=32)     latent→agent routing (inverse)

Replaces SimpleDirectoryMemory (numpy frequency table) and eliminates the only
non-Pineda memory in the pipeline.
"""

import io
import sys
import math
import contextlib
from pathlib import Path

import numpy as np

# Make hetero_lib importable.
_HETERO_DIR = Path(__file__).parent / "hetero_lib"
if str(_HETERO_DIR) not in sys.path:
    sys.path.insert(0, str(_HETERO_DIR))

import commons
from associative import AssociativeMemory


class PinedaAssociativeMemory:
    """
    Thin wrapper around AssociativeMemory from Pineda & Morales.

    Provides a clean public API, suppresses constructor output, and
    normalises the recog_weights return to a plain numpy array.

    Parameters
    ----------
    n : int  — number of features (domain size)
    m : int  — quantization levels per feature (range size)
    iota, kappa, xi, sigma — ExperimentSettings knobs (default 0/0/0/0.1)
    """

    def __init__(self, n: int, m: int,
                 iota: float = 0.0, kappa: float = 0.0,
                 xi: int = 0, sigma: float = 0.1):
        es = commons.ExperimentSettings(iota=iota, kappa=kappa, xi=xi, sigma=sigma)
        with contextlib.redirect_stdout(io.StringIO()):
            self._am = AssociativeMemory(n=n, m=m, es=es)
        self._n = n
        self._m = m

    # ------------------------------------------------------------------
    # Basic properties
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def register(self, cue_q: np.ndarray) -> None:
        """Register one quantized pattern."""
        v = self._am.validate(cue_q)
        r = self._am.to_relation(v)
        self._am.abstract(r)

    def recognize(self, cue_q: np.ndarray) -> float:
        """
        Returns mean recognition weight (raw count-based score).
        The bool recognized flag is intentionally ignored so this can
        always be used as a routing score even for unseen patterns.
        """
        _, weight = self._am.recognize(cue_q)
        return float(weight)

    def recog_weights(self, cue_q: np.ndarray) -> np.ndarray:
        """
        Per-feature recognition weights (shape: n).
        Used to modulate hetero-associative recognition following
        Pineda's architecture: left_eam.recog_weights → hetero_eam.
        Returns zeros for unseen patterns (caller should handle gracefully).
        """
        _, weights = self._am.recog_weights(cue_q)
        return np.asarray(weights, dtype=float)

    def recall(self, cue_q: np.ndarray):
        """
        Homo-associative recall.
        Returns (r_io, recognized: bool, weight: float).
        """
        r_io, recognized, weight = self._am.recall(cue_q)
        return r_io, bool(recognized), float(weight)

    def print_stats(self, name: str = "") -> None:
        print(f"[AM {name}] n={self._n} m={self._m} "
              f"entropy={self.entropy:.4f}  mean={self.mean:.4f}")


# ======================================================================
# Directory Memory
# ======================================================================

class PinedaDirectoryMemory:
    """
    M_dir: maps label/latent patterns → agent index via n_agents
    independent AssociativeMemory instances (one per agent slot).

    Routing logic
    -------------
    • register(v_q, j): record that pattern v_q routes to agent j
                        by storing v_q in _ams[j]
    • predict(v_q):     return recognition weight from each agent's AM
    • nearest_agent(v_q): argmax of predict() ; -1 if all scores zero

    B1 / B2 normalization (ablation)
    ----------------------------------
    predict_normalized(v_q, mode):
        'linear' (B1) : scores / (count_j + eps)
        'sqrt'   (B2) : scores / (√count_j + eps)
    """

    def __init__(self, n: int = 300, m: int = 16, n_agents: int = 3,
                 iota: float = 0.0, kappa: float = 0.0,
                 xi: int = 0, sigma: float = 0.1):
        self._n       = n
        self._m       = m
        self._n_agents = n_agents
        am_kw = dict(iota=iota, kappa=kappa, xi=xi, sigma=sigma)
        self._ams    = [PinedaAssociativeMemory(n, m, **am_kw)
                        for _ in range(n_agents)]
        # Registration counts per agent (for B1/B2 normalization)
        self._counts = np.zeros(n_agents, dtype=np.int64)

    # ------------------------------------------------------------------
    # Core API (matches SimpleDirectoryMemory interface)
    # ------------------------------------------------------------------

    def register(self, v_q: np.ndarray, agent_idx: int) -> None:
        """Record that pattern v_q routes to agent agent_idx."""
        k = int(np.clip(agent_idx, 0, self._n_agents - 1))
        self._ams[k].register(v_q)
        self._counts[k] += 1

    def predict(self, v_q: np.ndarray) -> np.ndarray:
        """Raw recognition scores per agent, shape (n_agents,)."""
        return np.array([am.recognize(v_q) for am in self._ams], dtype=float)

    def predict_normalized(self, v_q: np.ndarray,
                           mode: str = "linear",
                           eps: float = 1.0) -> np.ndarray:
        """
        Normalised routing scores.
        mode='linear' (B1): scores / (count + eps)
        mode='sqrt'   (B2): scores / (sqrt(count) + eps)
        """
        scores = self.predict(v_q)
        denom  = self._counts.astype(float) + eps
        return scores / denom if mode == "linear" else scores / np.sqrt(denom)

    def nearest_agent(self, v_q: np.ndarray) -> int:
        """Returns argmax agent index, or -1 if all scores are zero."""
        scores = self.predict(v_q)
        return -1 if scores.sum() == 0 else int(np.argmax(scores))

    # ------------------------------------------------------------------
    # Stats helpers (used by ablation + app)
    # ------------------------------------------------------------------

    @property
    def agent_counts(self) -> np.ndarray:
        return self._counts.copy()

    def entropy(self) -> float:
        total = float(self._counts.sum())
        if total == 0:
            return math.log2(max(self._n_agents, 1))
        p = self._counts / total
        return float(-np.sum(p * np.log2(np.where(p == 0, 1.0, p))))

    def print_stats(self, name: str = "") -> None:
        print(f"[DirMem {name}] counts={self._counts.tolist()} "
              f"entropy={self.entropy():.3f} bits")


# ------------------------------------------------------------------
# Backward-compatibility alias (pickle files referencing the old
# class name still work transparently).
# ------------------------------------------------------------------
SimpleDirectoryMemory = PinedaDirectoryMemory
