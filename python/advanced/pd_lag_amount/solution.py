from __future__ import annotations

import pandas as pd
def pd_lag_amount(frame: pd.DataFrame):
    """Lag amount within customer."""
    return frame.groupby('customer_id', sort=False)['amount'].shift(1)
