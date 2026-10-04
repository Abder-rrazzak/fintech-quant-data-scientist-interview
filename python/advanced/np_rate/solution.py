from __future__ import annotations

import numpy as np
def np_rate(flags: np.ndarray):
    """Mean of a binary array."""
    flags = np.asarray(flags, dtype=float)
    if len(flags) == 0:
        return 0.0
    return float(flags.mean())
