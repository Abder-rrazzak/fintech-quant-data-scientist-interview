from __future__ import annotations

import numpy as np
def np_sigmoid(logits: np.ndarray):
    """Vectorized sigmoid."""
    x = np.clip(np.asarray(logits, dtype=float), -30, 30)
    return 1.0 / (1.0 + np.exp(-x))
