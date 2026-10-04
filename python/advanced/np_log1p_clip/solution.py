from __future__ import annotations

import numpy as np
def np_log1p_clip(amounts: np.ndarray):
    """Vectorized log1p."""
    return np.log1p(np.clip(np.asarray(amounts, dtype=float), 0, None))
