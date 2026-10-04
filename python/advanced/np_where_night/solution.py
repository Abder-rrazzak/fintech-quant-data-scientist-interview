from __future__ import annotations

import numpy as np
def np_where_night(hours: np.ndarray):
    """Vectorized night flag."""
    hours = np.asarray(hours)
    return np.where((hours >= 0) & (hours <= 5), 1, 0)
