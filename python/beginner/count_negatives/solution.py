from __future__ import annotations

def count_negatives(amounts: list[float]):
    """Count negative amounts."""
    return sum(amount < 0 for amount in amounts)
