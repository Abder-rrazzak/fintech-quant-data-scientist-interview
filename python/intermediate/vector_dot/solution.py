from __future__ import annotations

def vector_dot(left: list[float], right: list[float]):
    """Dot product."""
    if len(left) != len(right):
        raise ValueError('length')
    return sum(a * b for a, b in zip(left, right))
