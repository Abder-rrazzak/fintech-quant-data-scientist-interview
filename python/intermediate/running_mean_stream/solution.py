from __future__ import annotations

def running_mean_stream(values: list[float]):
    """Streaming running mean."""
    total = 0.0
    for i, value in enumerate(values, start=1):
        total += value
        yield total / i
