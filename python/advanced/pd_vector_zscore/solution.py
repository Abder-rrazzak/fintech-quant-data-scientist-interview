from __future__ import annotations

import pandas as pd
def pd_vector_zscore(frame: pd.DataFrame):
    """Vectorized z-score."""
    std = frame['amount'].std(ddof=0)
    if std == 0 or pd.isna(std):
        return frame['amount'] * 0.0
    return (frame['amount'] - frame['amount'].mean()) / std
