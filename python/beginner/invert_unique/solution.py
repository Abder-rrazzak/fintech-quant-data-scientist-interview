from __future__ import annotations

def invert_unique(mapping: dict[str, str]):
    """Invert a unique map."""
    out = {}
    for key, value in mapping.items():
        if value in out:
            raise ValueError(value)
        out[value] = key
    return out
