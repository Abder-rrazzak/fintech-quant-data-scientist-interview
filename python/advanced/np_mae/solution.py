from __future__ import annotations

import numpy as np
def np_mae(y_true: np.ndarray, y_pred: np.ndarray):
    """Mean absolute error."""
    return float(np.mean(np.abs(np.asarray(y_true, dtype=float) - np.asarray(y_pred, dtype=float))))
