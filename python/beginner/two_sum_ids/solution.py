from __future__ import annotations

def two_sum_ids(amounts: list[float], target: float):
    """Two amounts that settle a target."""
    seen = {}
    for index, amount in enumerate(amounts):
        need = target - amount
        if need in seen:
            return [seen[need], index]
        seen[amount] = index
    return None
