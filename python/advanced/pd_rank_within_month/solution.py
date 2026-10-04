from __future__ import annotations

import pandas as pd
def pd_rank_within_month(frame: pd.DataFrame):
    """Rank within month."""
    out = frame.copy()
    out['rank_in_month'] = out.groupby('month')['amount'].rank(method='dense', ascending=False)
    return out
