from __future__ import annotations

import numpy as np
def np_lag_matrix(values: np.ndarray, lags: int):
    """Lag matrix."""
    values = np.asarray(values, dtype=float)
    rows = [values[t - lags:t][::-1] for t in range(lags, len(values))]
    targets = [values[t] for t in range(lags, len(values))]
    return np.asarray(rows, dtype=float), np.asarray(targets, dtype=float)
