from __future__ import annotations

import pandas as pd
def pd_query_large(frame: pd.DataFrame, threshold: float):
    """Filter large amounts."""
    return frame.loc[frame['amount'] > threshold].reset_index(drop=True)
