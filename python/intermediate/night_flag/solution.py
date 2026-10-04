from __future__ import annotations

def night_flag(hour: int):
    """Night flag."""
    if hour < 0 or hour > 23:
        raise ValueError('hour')
    return int(hour <= 5)
