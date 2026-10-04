from __future__ import annotations

import pandas as pd
def pd_asof_utilization(entities: pd.DataFrame, history: pd.DataFrame):
    """Backward as-of utilization."""
    left = entities.sort_values('as_of')
    right = history.sort_values('event_time')
    return pd.merge_asof(left, right, left_on='as_of', right_on='event_time', by='customer_id', direction='backward')
