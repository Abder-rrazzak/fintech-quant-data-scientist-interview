from __future__ import annotations

import pandas as pd
def pd_cutoff_features(frame: pd.DataFrame, cutoff: str):
    """Drop rows on or after a cutoff."""
    stamps = pd.to_datetime(frame['timestamp'])
    return frame.loc[stamps < pd.Timestamp(cutoff)].reset_index(drop=True)
