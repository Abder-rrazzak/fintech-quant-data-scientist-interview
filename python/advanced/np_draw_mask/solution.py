from __future__ import annotations

import numpy as np
def np_draw_mask(n: int, seed: int):
    """Reproducible bootstrap indexes."""
    rng = np.random.default_rng(seed)
    return rng.integers(0, n, size=n)
