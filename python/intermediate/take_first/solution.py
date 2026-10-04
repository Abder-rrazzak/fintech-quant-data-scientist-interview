from __future__ import annotations

def take_first(items, n: int):
    """Take the first n items."""
    if n < 0:
        raise ValueError('n')
    out = []
    for item in items:
        if len(out) == n:
            break
        out.append(item)
    return out
