from __future__ import annotations

import pandas as pd
def pd_drop_duplicate_ids(frame: pd.DataFrame):
    """Drop duplicate ids in pandas."""
    return frame.drop_duplicates('transaction_id', keep='first').reset_index(drop=True)
