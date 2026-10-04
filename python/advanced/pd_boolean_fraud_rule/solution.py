from __future__ import annotations

import pandas as pd
def pd_boolean_fraud_rule(frame: pd.DataFrame):
    """Boolean fraud rule in pandas."""
    return (frame['amount_zscore'] >= 3) | (frame['txn_count_1h'] >= 5)
