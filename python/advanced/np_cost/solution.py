from __future__ import annotations

import numpy as np
def np_cost(y_true: np.ndarray, scores: np.ndarray, threshold: float, fp_cost: float, fn_cost: float):
    """Vectorized business cost."""
    y_true = np.asarray(y_true).astype(int)
    pred = np.asarray(scores, dtype=float) >= threshold
    fp = int((pred & (y_true == 0)).sum())
    fn = int((~pred & (y_true == 1)).sum())
    return fp * fp_cost + fn * fn_cost
