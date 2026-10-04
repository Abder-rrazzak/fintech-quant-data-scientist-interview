from __future__ import annotations

import numpy as np
def np_safe_divide(numerator: np.ndarray, denominator: np.ndarray, fill: float = 0.0):
    """Vectorized safe divide."""
    numerator = np.asarray(numerator, dtype=float)
    denominator = np.asarray(denominator, dtype=float)
    out = np.full(numerator.shape, fill, dtype=float)
    mask = denominator != 0
    out[mask] = numerator[mask] / denominator[mask]
    return out
