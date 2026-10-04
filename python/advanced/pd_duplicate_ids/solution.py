from __future__ import annotations

import pandas as pd
def pd_duplicate_ids(frame: pd.DataFrame):
    """Duplicate transaction ids."""
    dupes = frame.loc[frame['transaction_id'].duplicated(keep=False), 'transaction_id']
    return sorted(dupes.unique().tolist())
