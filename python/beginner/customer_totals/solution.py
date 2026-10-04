from __future__ import annotations

def customer_totals(pairs: list[tuple[int, float]]):
    """Totals from pairs."""
    totals = {}
    for customer_id, amount in pairs:
        totals[customer_id] = totals.get(customer_id, 0.0) + amount
    return totals
