from __future__ import annotations

import pandas as pd
def pd_clip_amount(frame: pd.DataFrame, low: float, high: float):
    """Clip the amount column."""
    out = frame.copy()
    out['amount'] = out['amount'].clip(low, high)
    return out
