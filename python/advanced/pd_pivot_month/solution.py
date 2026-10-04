from __future__ import annotations

import pandas as pd
def pd_pivot_month(frame: pd.DataFrame):
    """Pivot monthly totals."""
    return frame.pivot_table(index='customer_id', columns='month', values='amount', aggfunc='sum', fill_value=0)
