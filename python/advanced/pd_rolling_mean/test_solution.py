import pandas as pd
from solution import pd_rolling_mean

def test_roll():
    frame = pd.DataFrame({'customer_id': [1, 1, 1], 'timestamp': [1, 2, 3], 'amount': [10.0, 20.0, 30.0]})
    out = pd_rolling_mean(frame)
    assert pd.isna(out.iloc[0]) and pd.isna(out.iloc[1])
    assert out.iloc[2] == 15.0
