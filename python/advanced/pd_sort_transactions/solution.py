from __future__ import annotations

import pandas as pd
def pd_sort_transactions(frame: pd.DataFrame):
    """Stable time sort."""
    return frame.sort_values(['customer_id', 'timestamp'], kind='mergesort').reset_index(drop=True)
