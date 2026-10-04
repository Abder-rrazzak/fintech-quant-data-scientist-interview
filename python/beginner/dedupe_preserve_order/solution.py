from __future__ import annotations

def dedupe_preserve_order(ids: list[int]):
    """Drop duplicate ids."""
    seen = set()
    out = []
    for item in ids:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out
