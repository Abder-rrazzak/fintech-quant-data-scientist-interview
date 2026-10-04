from __future__ import annotations

def csv_amount_sum(text: str):
    """Sum a CSV amount column."""
    lines = [line for line in text.splitlines() if line.strip()]
    header = lines[0].split(',')
    idx = header.index('amount')
    return sum(float(line.split(',')[idx]) for line in lines[1:])
