from __future__ import annotations

def all_customers(left: list[int], right: list[int]):
    """Union of customer ids."""
    return sorted(set(left) | set(right))
