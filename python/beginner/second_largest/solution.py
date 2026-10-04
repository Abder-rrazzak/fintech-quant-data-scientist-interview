from __future__ import annotations

def second_largest(amounts: list[float]):
    """Second largest distinct amount."""
    unique = sorted(set(amounts), reverse=True)
    return unique[1] if len(unique) > 1 else None
