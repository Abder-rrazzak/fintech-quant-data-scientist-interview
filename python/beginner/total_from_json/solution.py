from __future__ import annotations

def total_from_json(payload: str):
    """Sum amounts in a JSON list."""
    import json
    rows = json.loads(payload)
    return float(sum(float(row['amount']) for row in rows))
