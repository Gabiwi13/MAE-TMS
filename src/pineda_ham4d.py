"""
PinedaHAM4D — adapter that uses HeteroAssociativeMemory4D from Pineda & Morales
(hetero/hetero_associative_4d.py) as the backing memory.

Changes vs SimpleHAM4D:
  - recall_from_left / recall_from_right: use sample_n_search_recall
    (127-iteration stochastic sampling + neighbourhood hill-climbing)
    instead of a single stochastic reduce.
  - recall_from_right_soft: now delegates to recall_from_right, which
    uses the containment-AND projection instead of sum projection.
  - register / project / containment: identical to the original.

The only modification to the upstream file (hetero_associative_4d.py) is
a 1-line guard that makes classifier loading conditional on fold != None,
allowing the memory to be instantiated without MNIST/EMNIST classifier
weights that are irrelevant to this domain.
"""
import sys
import math
import numpy as np
from pathlib import Path

# Make hetero_lib/ importable (commons, associative are bare imports there).
# hetero_lib/ contains the three files from Pineda & Morales needed here,
# with the single-line patch to hetero_associative_4d.py (fold=None guard).
_HETERO_DIR = Path(__file__).parent / "hetero_lib"
if str(_HETERO_DIR) not in sys.path:
    sys.path.insert(0, str(_HETERO_DIR))

import commons
from hetero_associative_4d import HeteroAssociativeMemory4D


class PinedaHAM4D(HeteroAssociativeMemory4D):
    """
    Drop-in replacement for SimpleHAM4D that delegates all mathematical
    operations to HeteroAssociativeMemory4D from Pineda & Morales.

    Constructor matches SimpleHAM4D's signature:
        PinedaHAM4D(n, m, p, q, iota, kappa, xi, sigma)

    Internally calls HeteroAssociativeMemory4D.__init__ with fold=None
    (no domain classifiers needed; recall_with_sampling_n_search is used).
    """

    def __init__(self, n: int, m: int, p: int, q: int,
                 iota: float = 0.0, kappa: float = 0.0,
                 xi: int = 0, sigma: float = 0.1):
        import io, contextlib
        es = commons.ExperimentSettings(iota=iota, kappa=kappa, xi=xi, sigma=sigma)
        # fold=None → classifier loading is skipped (1-line patch in upstream).
        # All tensor initialisation (relation, iota_relation, margins, qudeqs)
        # runs exactly as in the original __init__. Output is suppressed to
        # avoid flooding the terminal during the ablation (180 × 3 instances).
        with contextlib.redirect_stdout(io.StringIO()):
            super().__init__(n=n, p=p, m=m, q=q, es=es, fold=None)

    def update(self):
        """Silent update — suppresses the verbose prints from the original."""
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            return super().update()

    # ------------------------------------------------------------------
    # Additional API required by this project (not in the original class)
    # ------------------------------------------------------------------

    def recognize_from_left(self, cue_a: np.ndarray,
                            left_weights: np.ndarray = None) -> float:
        """
        One-sided recognition score for agent routing (argmax across agents).

        Projects cue_a through the containment-AND relation (same project()
        as the original) and returns mean activation weight.

        Parameters
        ----------
        cue_a        : quantized left-domain cue (n-dimensional)
        left_weights : per-feature weights from M_dom_L.recog_weights().
                       When provided, modulates each feature's contribution
                       following Pineda's left_eam→hetero_eam architecture.
                       Normalised internally to [0, 1].
                       Falls back to uniform weights when None or all-zero.
        """
        ca = self.validate(cue_a, 0)
        if left_weights is None:
            weights = np.ones(len(ca), dtype=float)
        else:
            w = np.asarray(left_weights, dtype=float)
            mx = w.max()
            # Fall back to uniform if M_dom_L is empty (all-zero weights)
            weights = (w / mx) if mx > 0 else np.ones(len(ca), dtype=float)
        projection = self.project(ca, weights, 0)   # (p, q) — uses AND
        total = np.sum(projection)
        count = np.count_nonzero(projection)
        return float(total / count) if count > 0 else 0.0

    # ------------------------------------------------------------------
    # API adapters: unwrap 5-value returns to the 3-value contract used
    # by stage5, stage6, stage7, stage8 and run_ablation.
    # ------------------------------------------------------------------

    def recall_from_left(self, cue_a: np.ndarray):
        """Recall right domain from left cue. Returns (r_io, recognized, weight)."""
        weights = np.ones(len(cue_a), dtype=float)
        r_io, recognized, weight, _proj, _stats = super().recall_from_left(
            cue_a, weights=weights)
        r_q = _to_int(r_io, self.q)
        return r_q, bool(recognized), float(weight)

    def recall_from_right(self, cue_b: np.ndarray):
        """Recall left domain from right cue. Returns (r_io, recognized, weight)."""
        weights = np.ones(len(cue_b), dtype=float)
        r_io, recognized, weight, _proj, _stats = super().recall_from_right(
            cue_b, weights=weights)
        r_q = _to_int(r_io, self.m)
        return r_q, bool(recognized), float(weight)

    def recall_from_right_soft(self, cue_b: np.ndarray):
        """
        Inverse recall: right cue → left domain (used in stage7).

        In SimpleHAM4D this used sum-projection (soft).  Here it delegates to
        recall_from_right() which uses the containment-AND projection from the
        original — the mechanistic difference this migration fixes.

        Returns (r_io, score) for backward compatibility with stage7.
        """
        r_q, recognized, weight = self.recall_from_right(cue_b)
        return r_q, weight

    # ------------------------------------------------------------------
    # Compatibility helpers
    # ------------------------------------------------------------------

    def print_stats(self, name: str = ""):
        print(f"[HAM4D {name}] entropy={self.entropy:.4f}  mean={self.mean:.4f}")


# ------------------------------------------------------------------
# Module-level alias so that pickle files that stored SimpleHAM4D
# instances can be unpickled transparently after the migration.
# ------------------------------------------------------------------
SimpleHAM4D = PinedaHAM4D


# ------------------------------------------------------------------
# Internal helper
# ------------------------------------------------------------------

def _to_int(r_io, sentinel: int) -> np.ndarray:
    """Convert revalidated float array (NaN = undefined) to int with sentinel."""
    arr = np.asarray(r_io, dtype=float)
    return np.where(np.isnan(arr), sentinel, arr).astype(np.int32)
