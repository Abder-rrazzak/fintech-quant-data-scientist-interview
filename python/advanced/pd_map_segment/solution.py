from __future__ import annotations

import pandas as pd
def pd_map_segment(frame: pd.DataFrame, mapping: dict[str, str]):
    """Map a segment code."""
    out = frame.copy()
    out['segment_name'] = out['customer_segment'].map(mapping).fillna('other')
    return out
