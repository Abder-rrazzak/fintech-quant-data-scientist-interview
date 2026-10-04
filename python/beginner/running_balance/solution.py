from __future__ import annotations

def running_balance(opening: float, amounts: list[float]):
    """Running balance."""
    balance = opening
    out = []
    for amount in amounts:
        balance += amount
        out.append(balance)
    return out
