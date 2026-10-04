from __future__ import annotations

import pandas as pd
def pd_join_indicator(left: pd.DataFrame, right: pd.DataFrame):
    """Join with indicator."""
    merged = left.merge(right, on='customer_id', how='outer', indicator=True)
    return merged['_merge'].value_counts().to_dict()
