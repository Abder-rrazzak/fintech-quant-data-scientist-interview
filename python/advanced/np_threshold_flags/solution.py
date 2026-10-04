from __future__ import annotations

import numpy as np
def np_threshold_flags(scores: np.ndarray, threshold: float):
    """Threshold flags."""
    return (np.asarray(scores, dtype=float) >= threshold).astype(int)
