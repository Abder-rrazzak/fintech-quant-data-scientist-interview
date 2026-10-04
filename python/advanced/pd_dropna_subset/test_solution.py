import pandas as pd
from solution import pd_dropna_subset

def test_drop():
    frame = pd.DataFrame({'timestamp': ['2024-01-01', None], 'amount': [1.0, 2.0]})
    assert len(pd_dropna_subset(frame)) == 1
