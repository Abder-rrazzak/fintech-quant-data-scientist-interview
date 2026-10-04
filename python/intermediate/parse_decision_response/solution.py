from __future__ import annotations

def parse_decision_response(payload: str):
    """Read a decision."""
    import json
    return str(json.loads(payload)['decision'])
