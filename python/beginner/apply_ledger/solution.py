from __future__ import annotations

def apply_ledger(opening: float, operations: list[tuple[str, float]]):
    """Apply deposit and withdraw operations."""
    balance = opening
    for op, amount in operations:
        if amount < 0:
            raise ValueError('amount')
        if op == 'deposit':
            balance += amount
        elif op == 'withdraw':
            if amount > balance:
                raise ValueError('insufficient')
            balance -= amount
        else:
            raise ValueError(op)
    return balance
