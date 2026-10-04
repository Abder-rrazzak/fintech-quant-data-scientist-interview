from __future__ import annotations

import pandas as pd
def pd_melt_balances(frame: pd.DataFrame):
    """Melt wide balances."""
    return frame.melt(id_vars=['customer_id'], value_vars=['balance_before', 'balance_after'], var_name='field', value_name='value')
