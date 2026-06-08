"""
Quantizer/dequantizer utilities.
Maps continuous vectors to discrete levels and back.
"""
import numpy as np


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
    """
    Quantize a binary {-1, +1} vector to [0, levels-1].
    -1 -> 0, +1 -> levels-1, intermediate values linearly.
    """
    v = (vec + 1.0) / 2.0   # [0, 1]
    q = np.floor(v * levels).astype(np.int32)
    q = np.clip(q, 0, levels - 1)
    return q


def dequantize(q: np.ndarray, levels: int,
               vmin: float = -1.0, vmax: float = 1.0) -> np.ndarray:
    """Inverse of quantize_binary — maps integers back to floats."""
    v = q.astype(float) / (levels - 1)   # [0, 1]
    return v * (vmax - vmin) + vmin
