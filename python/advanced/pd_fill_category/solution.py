from __future__ import annotations

import pandas as pd
def pd_fill_category(frame: pd.DataFrame):
    """Fill missing categories."""
    out = frame.copy()
    out['merchant_category'] = out['merchant_category'].fillna('unknown')
    return out
