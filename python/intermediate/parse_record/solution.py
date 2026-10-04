from __future__ import annotations

def parse_record(record: dict[str, object]):
    """Parse a record."""
    return int(record['customer_id']), float(record['amount'])
