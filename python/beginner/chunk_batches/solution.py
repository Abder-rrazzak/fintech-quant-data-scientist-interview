from __future__ import annotations

def chunk_batches(items: list[int], size: int):
    """Chunk a list."""
    if size <= 0:
        raise ValueError('size')
    return [items[i:i + size] for i in range(0, len(items), size)]
