from __future__ import annotations

import pandas as pd
def pd_memory_bytes(frame: pd.DataFrame):
    """Estimate frame memory."""
    return int(frame.memory_usage(deep=True).sum())
