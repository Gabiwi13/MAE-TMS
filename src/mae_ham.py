"""
SimpleHAM4D — redirected to PinedaHAM4D (HeteroAssociativeMemory4D from Pineda & Morales).

The original numpy-only implementation is preserved below for reference.
All new code imports SimpleHAM4D from this module and receives PinedaHAM4D.
"""
# Migration: use Pineda's original implementation.
from pineda_ham4d import PinedaHAM4D as SimpleHAM4D  # noqa: F401

# ── Original implementation kept for reference ──────────────────────────────
import math
import random
import numpy as np


class _OriginalSimpleHAM4D:
    """
    Original numpy-only implementation — kept for reference only.
    Use SimpleHAM4D (= PinedaHAM4D) for all new code.

    Hetero-associative memory between two domains:
      Domain A (left):  n features, m quantization levels  -> label space
      Domain B (right): p features, q quantization levels  -> latent space
    """

    def __init__(self, n: int, m: int, p: int, q: int,
                 iota: float = 0.0, kappa: float = 0.0,
                 xi: int = 0, sigma: float = 0.1):
        self._n = n
        self._p = p
        self._m = m + 1  # +1 for partial-function sentinel
        self._q = q + 1
        self._iota = iota
        self._kappa = kappa
        self._xi = xi
        self._sigma = sigma
        self._absolute_max = 2 ** 16 - 1

        # Core 4D relation tensor
        self._relation = np.zeros((n, p, self._m, self._q), dtype=np.int32)
        self._iota_relation = np.zeros((n, p, self._m, self._q), dtype=np.int32)
        self._entropies = np.zeros((n, p), dtype=np.float64)
        self._means = np.zeros((n, p), dtype=np.float64)
        self._updated = True
        self._set_margins()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def n(self): return self._n

    @property
    def p(self): return self._p

    @property
    def m(self): return self._m - 1

    @property
    def q(self): return self._q - 1

    @property
    def entropy(self):
        if not self._updated:
            self._update()
        return float(np.mean(self._entropies))

    @property
    def mean(self):
        if not self._updated:
            self._update()
        return float(np.mean(self._means))

    @property
    def _full_iota_relation(self):
        if not self._updated:
            self._update()
        return self._iota_relation

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register(self, cue_a: np.ndarray, cue_b: np.ndarray) -> None:
        """Store one association (cue_a in A, cue_b in B)."""
        ca = self._validate(cue_a, 0)
        cb = self._validate(cue_b, 1)
        r = self._vectors_to_relation(ca, cb)
        self._abstract(r)

    def recognize_from_left(self, cue_a: np.ndarray) -> float:
        """
        One-sided recognition: project left cue onto stored relation,
        return mean activation weight (used for argmax across agents).
        """
        ca = self._validate(cue_a, 0)
        proj = self._project_left(ca)
        # mean over all (p, q) cells that are non-zero
        total = np.sum(proj)
        count = np.count_nonzero(proj)
        if count == 0:
            return 0.0
        return float(total / count)

    def recall_from_left(self, cue_a: np.ndarray):
        """
        Given a left cue (label), recall the right cue (latent vector).
        Returns (recalled_cue_b, recognized: bool, weight: float).
        """
        ca = self._validate(cue_a, 0)
        proj = self._project_left(ca)
        recognized = np.count_nonzero(np.sum(proj, axis=1) == 0) == 0
        if not recognized:
            return np.full(self._p, self.q, dtype=np.int32), False, 0.0
        r_io, weights = self._reduce(proj, 1)
        weight = float(np.mean(weights))
        return r_io, True, weight

    def recall_from_right(self, cue_b: np.ndarray):
        """
        Given a right cue (latent), recall the left cue (label vector).
        Returns (recalled_cue_a, recognized: bool, weight: float).
        """
        cb = self._validate(cue_b, 1)
        proj = self._project_right(cb)
        recognized = np.count_nonzero(np.sum(proj, axis=1) == 0) == 0
        if not recognized:
            return np.full(self._n, self.m, dtype=np.int32), False, 0.0
        r_io, weights = self._reduce(proj, 0)
        weight = float(np.mean(weights))
        return r_io, True, weight

    def recall_from_right_soft(self, cue_b: np.ndarray):
        """
        Soft projection (sum, not AND) for inverse retrieval from unseen latents.
        Tolerates deviation from the stored prototype.
        Returns (recalled_cue_a, score: float).
        """
        cb = self._validate(cue_b, 1)
        ir = self._full_iota_relation
        # Use shape (n, m) without the undefined sentinel row
        integration = np.zeros((self._n, self.m), dtype=float)
        for j in range(self._p):
            k = cb[j]
            if k == self.q:
                continue
            integration += ir[:, j, :self.m, k].astype(float)
        total = np.sum(integration)
        if total == 0:
            return np.full(self._n, self.m, dtype=np.int32), 0.0
        r_io, weights = self._reduce(integration, 0)
        return r_io, float(np.mean(weights))

    def print_stats(self, name: str = ""):
        if not self._updated:
            self._update()
        print(f"[HAM4D {name}] entropy={self.entropy:.4f}  mean={self.mean:.4f}  "
              f"fullness={self._fullness():.4f}")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _set_margins(self):
        self._relation[:, :, self.m, :] = 1
        self._relation[:, :, :, self.q] = 1
        self._iota_relation[:, :, self.m, :] = 1
        self._iota_relation[:, :, :, self.q] = 1

    def _abstract(self, r_io):
        self._relation = np.where(
            self._relation == self._absolute_max,
            self._relation, self._relation + r_io)
        self._updated = False

    def _vectors_to_relation(self, ca, cb):
        r = np.zeros((self._n, self._p, self._m, self._q), dtype=np.int32)
        for i in range(self._n):
            k = ca[i]
            for j in range(self._p):
                label = cb[j]
                r[i, j, k, label] = 1
        return r

    def _project_left(self, ca: np.ndarray) -> np.ndarray:
        """Project left cue onto (p, q) space."""
        ir = self._full_iota_relation
        integration = np.zeros((self._p, self._q), dtype=float)
        first = True
        for i in range(self._n):
            k = ca[i]
            if k == self.m:  # undefined
                continue
            col = ir[i, :, k, :self.q]  # shape (p, q)
            if first:
                integration = col.astype(float)
                first = False
            else:
                integration = np.where(
                    (integration == 0) | (col == 0),
                    0, integration + col)
        return integration

    def _project_right(self, cb: np.ndarray) -> np.ndarray:
        """Project right cue onto (n, m) space."""
        ir = self._full_iota_relation
        integration = np.zeros((self._n, self._m), dtype=float)
        first = True
        for j in range(self._p):
            k = cb[j]
            if k == self.q:  # undefined
                continue
            col = ir[:, j, :self.m, k]  # shape (n, m)
            if first:
                integration = col.astype(float)
                first = False
            else:
                integration = np.where(
                    (integration == 0) | (col == 0),
                    0, integration + col)
        return integration

    def _reduce(self, projection: np.ndarray, dim: int):
        """Reduce a relation to a function by sampling each column."""
        cols = self._n if dim == 0 else self._p
        undef = self.m if dim == 0 else self.q
        v = np.zeros(cols, dtype=np.int32)
        weights = np.zeros(cols, dtype=float)
        for i in range(cols):
            col = projection[i]
            s = col.sum()
            if s == 0:
                v[i] = undef
                weights[i] = 0.0
            else:
                r = s * random.random()
                chosen = undef
                for j in range(col.size):   # use actual column length
                    if r <= col[j]:
                        chosen = j
                        break
                    r -= col[j]
                v[i] = chosen
                weights[i] = col[chosen] if chosen != undef else 0.0
        return v, weights

    def _validate(self, cue: np.ndarray, dim: int) -> np.ndarray:
        expected = self._n if dim == 0 else self._p
        rows = self.m if dim == 0 else self.q
        if cue.size != expected:
            raise ValueError(
                f"Expected length {expected} for dim {dim}, got {cue.size}")
        v = np.clip(cue, 0, rows - 1)
        v = np.nan_to_num(v, nan=rows)
        return v.round().astype(np.int32)

    def _fullness(self) -> float:
        count = np.count_nonzero(self._relation[:, :, :self.m, :self.q])
        total = self._n * self._p * self.m * self.q
        return count / total if total > 0 else 0.0

    def _update(self):
        self._update_entropies()
        self._update_means()
        self._update_iota_relation()
        self._updated = True

    def _update_entropies(self):
        rel = self._relation[:, :, :self.m, :self.q]
        for i in range(self._n):
            for j in range(self._p):
                r = rel[i, j]
                total = np.sum(r)
                if total > 0:
                    p = r / total
                    self._entropies[i, j] = -np.sum(
                        p * np.log2(np.where(p == 0, 1.0, p)))
                else:
                    self._entropies[i, j] = 0.0

    def _update_means(self):
        rel = self._relation[:, :, :self.m, :self.q]
        for i in range(self._n):
            for j in range(self._p):
                r = rel[i, j]
                count = np.count_nonzero(r)
                count = 1 if count == 0 else count
                self._means[i, j] = np.sum(r) / count

    def _update_iota_relation(self):
        rel = self._relation[:, :, :self.m, :self.q]
        for i in range(self._n):
            for j in range(self._p):
                r = rel[i, j]
                s = np.sum(r)
                if s == 0:
                    self._iota_relation[i, j, :self.m, :self.q] = 0
                else:
                    count = max(1, np.count_nonzero(r))
                    threshold = self._iota * s / count
                    self._iota_relation[i, j, :self.m, :self.q] = np.where(
                        r < threshold, 0, r)
        # keep margins
        self._iota_relation[:, :, self.m, :] = 1
        self._iota_relation[:, :, :, self.q] = 1
