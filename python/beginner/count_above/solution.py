from __future__ import annotations

def count_above(amounts: list[float], threshold: float):
    """Count amounts above a threshold."""
    return sum(amount > threshold for amount in amounts)
