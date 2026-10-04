from __future__ import annotations

import pandas as pd
def pd_fraud_rate(frame: pd.DataFrame):
    """Fraud rate by segment."""
    return frame.groupby('customer_segment', sort=True)['is_fraud'].mean()
