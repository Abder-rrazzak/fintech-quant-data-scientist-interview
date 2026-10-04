from __future__ import annotations

import numpy as np
def np_log_returns(prices: np.ndarray):
    """NumPy log returns."""
    prices = np.asarray(prices, dtype=float)
    if np.any(prices <= 0):
        raise ValueError('price')
    return np.diff(np.log(prices))
