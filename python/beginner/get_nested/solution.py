from __future__ import annotations

def get_nested(mapping: dict, outer: str, inner: str, default: float):
    """Read a nested field."""
    inner_map = mapping.get(outer)
    if not isinstance(inner_map, dict) or inner not in inner_map:
        return default
    return inner_map[inner]
