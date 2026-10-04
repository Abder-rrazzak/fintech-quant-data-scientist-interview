import pandas as pd
from solution import pd_expanding_sum

def test_exp():
    frame = pd.DataFrame({'customer_id': [1, 1], 'amount': [2.0, 5.0]})
    assert pd_expanding_sum(frame).tolist() == [2.0, 7.0]
