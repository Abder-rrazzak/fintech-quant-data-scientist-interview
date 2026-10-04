from __future__ import annotations

def sigmoid_score(value: float):
    """Safe sigmoid."""
    import math
    x = min(max(value, -30.0), 30.0)
    return 1.0 / (1.0 + math.exp(-x))
