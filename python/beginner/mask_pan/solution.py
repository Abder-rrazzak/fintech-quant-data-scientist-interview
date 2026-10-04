from __future__ import annotations

def mask_pan(pan: str):
    """Mask a card number."""
    if len(pan) <= 4:
        return pan
    return '*' * (len(pan) - 4) + pan[-4:]
