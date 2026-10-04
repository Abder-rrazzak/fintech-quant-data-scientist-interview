from __future__ import annotations

def time_split_indexes(n: int):
    """Time split indexes."""
    if n < 3:
        raise ValueError('n')
    train_end = max(1, int(n * 0.70))
    valid_end = min(n - 1, max(train_end + 1, int(n * 0.85)))
    return train_end, valid_end
