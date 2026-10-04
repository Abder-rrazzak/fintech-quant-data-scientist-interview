from __future__ import annotations

import pandas as pd
def pd_customer_totals(frame: pd.DataFrame):
    """Pandas customer totals."""
    return frame.groupby('customer_id', sort=True)['amount'].sum()
