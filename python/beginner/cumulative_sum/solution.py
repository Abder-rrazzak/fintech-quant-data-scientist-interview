from __future__ import annotations

def cumulative_sum(amounts: list[float]):
    """Cumulative sum."""
    total = 0.0
    out = []
    for amount in amounts:
        total += amount
        out.append(total)
    return out
