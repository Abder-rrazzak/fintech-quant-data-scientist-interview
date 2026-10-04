from __future__ import annotations

import numpy as np
def np_argmax_amount(amounts: np.ndarray):
    """Index of the largest amount."""
    return int(np.argmax(np.asarray(amounts, dtype=float)))
