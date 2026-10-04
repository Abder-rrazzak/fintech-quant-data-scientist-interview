from __future__ import annotations

def merge_amount_dicts(left: dict[str, float], right: dict[str, float]):
    """Merge amount maps."""
    out = dict(left)
    for key, value in right.items():
        out[key] = out.get(key, 0.0) + value
    return out
