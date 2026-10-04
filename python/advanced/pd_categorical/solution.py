from __future__ import annotations

import pandas as pd
def pd_categorical(frame: pd.DataFrame, categories: list[str]):
    """Categorical merchant category."""
    out = frame.copy()
    out['merchant_category'] = pd.Categorical(out['merchant_category'], categories=categories)
    return out
