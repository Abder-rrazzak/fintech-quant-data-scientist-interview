from __future__ import annotations

def non_negative(func):
    """Reject negative amounts."""
    def wrapper(value, *args, **kwargs):
        if value < 0:
            raise ValueError('negative')
        return func(value, *args, **kwargs)
    return wrapper
