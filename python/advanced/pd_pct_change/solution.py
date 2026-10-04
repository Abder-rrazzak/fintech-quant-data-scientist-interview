from __future__ import annotations

import pandas as pd
def pd_pct_change(frame: pd.DataFrame):
    """Percent change within customer."""
    return frame.groupby('customer_id', sort=False)['amount'].pct_change()
