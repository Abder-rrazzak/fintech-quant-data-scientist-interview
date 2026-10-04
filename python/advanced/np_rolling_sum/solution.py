from __future__ import annotations

import numpy as np
def np_rolling_sum(values: np.ndarray, k: int):
    """NumPy rolling sum."""
    values = np.asarray(values, dtype=float)
    if k <= 0 or k > len(values):
        raise ValueError('k')
    window = np.ones(k)
    return np.convolve(values, window, mode='valid')
