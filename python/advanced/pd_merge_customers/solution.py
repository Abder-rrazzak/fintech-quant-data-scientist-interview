from __future__ import annotations

import pandas as pd
def pd_merge_customers(transactions: pd.DataFrame, customers: pd.DataFrame):
    """Merge transactions to customers."""
    return transactions.merge(customers, on='customer_id', how='left')
