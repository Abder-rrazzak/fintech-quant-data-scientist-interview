from __future__ import annotations

import pandas as pd
def pd_cohort_month(frame: pd.DataFrame):
    """Signup cohort."""
    return pd.to_datetime(frame['signup_date']).dt.to_period('M').astype(str)
