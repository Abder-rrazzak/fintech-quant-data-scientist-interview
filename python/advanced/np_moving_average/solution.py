from __future__ import annotations

import numpy as np
def np_moving_average(values: np.ndarray, k: int):
    """Moving average."""
    values = np.asarray(values, dtype=float)
    if k <= 0 or k > len(values):
        raise ValueError('k')
    kernel = np.ones(k) / k
    return np.convolve(values, kernel, mode='valid')
