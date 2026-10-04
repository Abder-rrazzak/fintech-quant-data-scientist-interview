from __future__ import annotations

def shared_customers(left: list[int], right: list[int]):
    """Customers in both months."""
    return sorted(set(left) & set(right))
