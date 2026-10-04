from __future__ import annotations

def first_index_above(amounts: list[float], limit: float):
    """First index above a limit."""
    for i, amount in enumerate(amounts):
        if amount > limit:
            return i
    return -1
