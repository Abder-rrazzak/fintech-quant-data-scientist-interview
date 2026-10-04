from __future__ import annotations

def score_payload(features: dict[str, float]):
    """Stable JSON payload."""
    import json
    return json.dumps(features, sort_keys=True)
