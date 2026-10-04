from __future__ import annotations

import numpy as np
def np_standardize_columns(features: np.ndarray):
    """Column standardize."""
    x = np.asarray(features, dtype=float)
    std = x.std(axis=0)
    centered = x - x.mean(axis=0)
    zero = std == 0
    centered[:, zero] = 0.0
    safe = np.where(zero, 1.0, std)
    return centered / safe
