from __future__ import annotations

def last4(value: str):
    """Last four characters."""
    if len(value) < 4:
        raise ValueError('short')
    return value[-4:]
