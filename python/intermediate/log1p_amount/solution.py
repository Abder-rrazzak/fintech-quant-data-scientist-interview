from __future__ import annotations

def log1p_amount(amount: float):
    """Log1p of a clipped amount."""
    import math
    return math.log1p(max(amount, 0.0))
