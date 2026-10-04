from __future__ import annotations

import pandas as pd
def pd_rolling_mean(frame: pd.DataFrame):
    """Rolling mean by customer."""
    shifted = frame.groupby('customer_id', sort=False)['amount'].shift(1)
    return shifted.groupby(frame['customer_id'], sort=False).rolling(2, min_periods=2).mean().reset_index(level=0, drop=True)
