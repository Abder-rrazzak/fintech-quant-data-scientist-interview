from __future__ import annotations

import pandas as pd
def pd_between_time(frame: pd.DataFrame, start: str, end: str):
    """Rows inside a time window."""
    stamps = pd.to_datetime(frame['timestamp'])
    mask = (stamps >= pd.Timestamp(start)) & (stamps < pd.Timestamp(end))
    return frame.loc[mask].reset_index(drop=True)
