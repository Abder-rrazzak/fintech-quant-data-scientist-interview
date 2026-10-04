import pandas as pd
from solution import pd_nunique_merchants

def test_nunique():
    frame = pd.DataFrame({'customer_id': [1, 1, 1], 'merchant_id': [5, 5, 9]})
    assert pd_nunique_merchants(frame).loc[1] == 2
