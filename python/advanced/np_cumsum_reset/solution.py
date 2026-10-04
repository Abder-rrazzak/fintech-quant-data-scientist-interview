from __future__ import annotations

import numpy as np
def np_cumsum_reset(values: np.ndarray):
    """Cumulative sum."""
    return np.cumsum(np.asarray(values, dtype=float))
