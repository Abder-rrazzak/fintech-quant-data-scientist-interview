from __future__ import annotations

def make_fee(fee: float):
    """Closure that adds a fixed fee."""
    def add_fee(amount: float) -> float:
        return amount + fee
    return add_fee
