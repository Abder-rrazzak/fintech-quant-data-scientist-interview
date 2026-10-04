from __future__ import annotations

import numpy as np
def np_one_hot(labels: np.ndarray, n_classes: int):
    """One-hot encode small integers."""
    labels = np.asarray(labels, dtype=int)
    out = np.zeros((len(labels), n_classes), dtype=float)
    out[np.arange(len(labels)), labels] = 1.0
    return out
