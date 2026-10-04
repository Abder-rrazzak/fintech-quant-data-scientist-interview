from __future__ import annotations

import pandas as pd
def pd_resample_daily(frame: pd.DataFrame):
    """Resample to daily totals."""
    indexed = frame.set_index('timestamp').sort_index()
    return indexed['amount'].resample('D').sum()
