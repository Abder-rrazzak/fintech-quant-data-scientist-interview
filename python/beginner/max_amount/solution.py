from __future__ import annotations

def max_amount(amounts: list[float]):
    """Largest amount."""
    if not amounts:
        raise ValueError('empty')
    return max(amounts)
