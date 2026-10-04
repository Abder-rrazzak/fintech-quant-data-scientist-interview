from __future__ import annotations

import pandas as pd
def pd_dropna_subset(frame: pd.DataFrame):
    """Drop rows missing keys."""
    return frame.dropna(subset=['timestamp', 'amount']).reset_index(drop=True)
