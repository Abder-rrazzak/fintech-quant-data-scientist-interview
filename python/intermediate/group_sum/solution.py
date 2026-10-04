from __future__ import annotations

def group_sum(rows: list[tuple[int, float]]):
    """Group and sum."""
    totals = {}
    for customer_id, amount in rows:
        totals[customer_id] = totals.get(customer_id, 0.0) + amount
    return totals
