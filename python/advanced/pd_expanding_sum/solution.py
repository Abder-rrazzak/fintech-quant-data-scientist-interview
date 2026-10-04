from __future__ import annotations

import pandas as pd
def pd_expanding_sum(frame: pd.DataFrame):
    """Expanding sum by customer."""
    return frame.groupby('customer_id', sort=False)['amount'].expanding().sum().reset_index(level=0, drop=True)
