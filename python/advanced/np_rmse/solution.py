from __future__ import annotations

import numpy as np
def np_rmse(y_true: np.ndarray, y_pred: np.ndarray):
    """Root mean squared error."""
    err = np.asarray(y_pred, dtype=float) - np.asarray(y_true, dtype=float)
    return float(np.sqrt(np.mean(err ** 2)))
