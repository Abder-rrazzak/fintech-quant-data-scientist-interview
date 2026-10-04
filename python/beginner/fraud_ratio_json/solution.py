from __future__ import annotations

def fraud_ratio_json(payload: str):
    """Fraud ratio from JSON."""
    import json
    rows = json.loads(payload)
    if not rows:
        return 0.0
    return sum(int(row['is_fraud']) for row in rows) / len(rows)
