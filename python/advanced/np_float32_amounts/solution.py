from __future__ import annotations

import numpy as np
def np_float32_amounts(amounts: np.ndarray):
    """Store amounts as float32."""
    return np.asarray(amounts, dtype=np.float32)
