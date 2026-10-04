from __future__ import annotations

import numpy as np
def np_zscore(values: np.ndarray):
    """NumPy z-score."""
    values = np.asarray(values, dtype=float)
    std = values.std()
    if std == 0:
        return np.zeros_like(values, dtype=float)
    return (values - values.mean()) / std
