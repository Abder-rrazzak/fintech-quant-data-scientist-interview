from __future__ import annotations

def pairwise_stream(values: list[float]):
    """Consecutive pairs."""
    for i in range(1, len(values)):
        yield (values[i - 1], values[i])
