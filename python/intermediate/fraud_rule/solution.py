from __future__ import annotations

def fraud_rule(amount_z: float, count_1h: int, geo_mismatch: int, new_device: int):
    """Transparent fraud rule."""
    return amount_z >= 3 or count_1h >= 5 or (geo_mismatch == 1 and new_device == 1)
