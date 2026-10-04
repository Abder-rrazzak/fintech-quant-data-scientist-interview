from __future__ import annotations

import pandas as pd
def pd_value_counts_norm(frame: pd.DataFrame):
    """Normalized value counts."""
    return frame['merchant_category'].value_counts(normalize=True).sort_index()
