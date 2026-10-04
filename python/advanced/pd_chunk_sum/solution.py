from __future__ import annotations

import pandas as pd
def pd_chunk_sum(path: str, chunksize: int = 2):
    """Sum a CSV in chunks."""
    total = 0.0
    for chunk in pd.read_csv(path, chunksize=chunksize, usecols=['amount']):
        total += float(chunk['amount'].sum())
    return total
