import pandas as pd
from solution import pd_rank_within_month

def test_rank():
    frame = pd.DataFrame({'month': ['m', 'm'], 'amount': [5.0, 9.0]})
    out = pd_rank_within_month(frame)
    assert out.loc[out['amount'] == 9.0, 'rank_in_month'].iloc[0] == 1
