from __future__ import annotations

import pandas as pd
def pd_month_key(frame: pd.DataFrame):
    """Month key."""
    return pd.to_datetime(frame['timestamp']).dt.strftime('%Y-%m')
