import pandas as pd
from solution import pd_lag_amount

def test_lag():
    frame = pd.DataFrame({'customer_id': [1, 1], 'amount': [4.0, 9.0]})
    out = pd_lag_amount(frame)
    assert pd.isna(out.iloc[0]) and out.iloc[1] == 4.0
