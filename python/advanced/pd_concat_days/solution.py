from __future__ import annotations

import pandas as pd
def pd_concat_days(frames: list[pd.DataFrame]):
    """Concatenate daily extracts."""
    return pd.concat(frames, ignore_index=True)
