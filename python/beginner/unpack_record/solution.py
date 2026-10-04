from __future__ import annotations

def unpack_record(record: tuple[int, float, str]):
    """Unpack a transaction triple."""
    customer_id, amount, country = record
    return {'customer_id': customer_id, 'amount': amount, 'country': country}
