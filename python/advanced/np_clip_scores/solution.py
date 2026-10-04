from __future__ import annotations

import numpy as np
def np_clip_scores(scores: np.ndarray):
    """Clip scores."""
    return np.clip(np.asarray(scores, dtype=float), 0.0, 1.0)
