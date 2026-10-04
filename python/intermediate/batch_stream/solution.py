from __future__ import annotations

def batch_stream(items: list[int], size: int):
    """Yield batches."""
    if size <= 0:
        raise ValueError('size')
    for i in range(0, len(items), size):
        yield items[i:i + size]
