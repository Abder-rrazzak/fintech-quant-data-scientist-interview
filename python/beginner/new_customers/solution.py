from __future__ import annotations

def new_customers(prior: list[int], current: list[int]):
    """Customers who appeared later."""
    return sorted(set(current) - set(prior))
