import pandas as pd
from solution import pd_melt_balances

def test_melt():
    frame = pd.DataFrame({'customer_id': [1], 'balance_before': [5.0], 'balance_after': [4.0]})
    out = pd_melt_balances(frame)
    assert set(out['field']) == {'balance_before', 'balance_after'}
