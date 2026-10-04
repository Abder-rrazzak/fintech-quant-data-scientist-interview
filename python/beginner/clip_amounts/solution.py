from __future__ import annotations

def clip_amounts(amounts: list[float], low: float, high: float):
    """Clip amounts into a range."""
    return [min(max(amount, low), high) for amount in amounts]
