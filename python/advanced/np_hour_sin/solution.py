from __future__ import annotations

import numpy as np
def np_hour_sin(hours: np.ndarray):
    """Cyclic hour encoding."""
    hours = np.asarray(hours, dtype=float)
    return np.sin(2 * np.pi * hours / 24.0)
