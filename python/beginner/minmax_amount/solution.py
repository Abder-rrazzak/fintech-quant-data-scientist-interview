from __future__ import annotations

def minmax_amount(amounts: list[float]):
    """Min and max as a tuple."""
    if not amounts:
        raise ValueError('empty')
    return (min(amounts), max(amounts))
