import pandas as pd
from solution import pd_cutoff_features

def test_cut():
    frame = pd.DataFrame({'timestamp': ['2024-01-01', '2024-08-01'], 'amount': [3.0, 9.0]})
    out = pd_cutoff_features(frame, '2024-06-01')
    assert out['amount'].tolist() == [3.0]
