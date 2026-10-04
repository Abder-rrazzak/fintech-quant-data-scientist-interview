import pandas as pd
from solution import pd_resample_daily

def test_resample():
    frame = pd.DataFrame({'timestamp': pd.to_datetime(['2024-01-01 01:00', '2024-01-01 05:00', '2024-01-02 01:00']), 'amount': [1.0, 2.0, 4.0]})
    out = pd_resample_daily(frame)
    assert out.iloc[0] == 3.0 and out.iloc[1] == 4.0
