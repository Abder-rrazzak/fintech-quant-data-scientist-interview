from __future__ import annotations

import numpy as np
def np_expanding_mean(values: np.ndarray):
    """Expanding mean."""
    values = np.asarray(values, dtype=float)
    return np.cumsum(values) / np.arange(1, len(values) + 1)
