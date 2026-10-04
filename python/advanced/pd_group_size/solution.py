from __future__ import annotations

import pandas as pd
def pd_group_size(frame: pd.DataFrame):
    """Transactions per customer."""
    return frame.groupby('customer_id', sort=True).size()
