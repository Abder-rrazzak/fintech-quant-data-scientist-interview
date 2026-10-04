from __future__ import annotations

def dedupe_rows(rows: list[dict]):
    """Drop duplicate transaction dicts."""
    seen = set()
    out = []
    for row in rows:
        key = row['transaction_id']
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out
