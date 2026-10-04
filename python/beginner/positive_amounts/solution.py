from __future__ import annotations

def positive_amounts(amounts: list[float]):
    """Keep positive amounts."""
    return [amount for amount in amounts if amount > 0]
