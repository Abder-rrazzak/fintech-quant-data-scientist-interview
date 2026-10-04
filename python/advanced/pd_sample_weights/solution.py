from __future__ import annotations

import pandas as pd
def pd_sample_weights(frame: pd.DataFrame):
    """Inverse-frequency weights."""
    counts = frame['is_fraud'].value_counts()
    return frame['is_fraud'].map(lambda label: 1.0 / counts[label])
