from __future__ import annotations

def safe_divide(numerator: float, denominator: float, default: float = 0.0):
    """Divide without crashing on zero."""
    if denominator == 0:
        return default
    return numerator / denominator
