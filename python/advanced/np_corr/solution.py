from __future__ import annotations

import numpy as np
def np_corr(left: np.ndarray, right: np.ndarray):
    """Pearson correlation."""
    left = np.asarray(left, dtype=float)
    right = np.asarray(right, dtype=float)
    if left.std() == 0 or right.std() == 0:
        raise ValueError('variance')
    return float(np.corrcoef(left, right)[0, 1])
