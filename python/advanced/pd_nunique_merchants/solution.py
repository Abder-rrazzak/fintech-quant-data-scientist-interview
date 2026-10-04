from __future__ import annotations

import pandas as pd
def pd_nunique_merchants(frame: pd.DataFrame):
    """Distinct merchants per customer."""
    return frame.groupby('customer_id', sort=True)['merchant_id'].nunique()
