import pandas as pd
from solution import pd_pct_change

def test_pct():
    frame = pd.DataFrame({'customer_id': [1, 1], 'amount': [10.0, 15.0]})
    out = pd_pct_change(frame)
    assert pd.isna(out.iloc[0]) and out.iloc[1] == 0.5
