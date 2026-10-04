import pandas as pd
from solution import pd_sort_transactions

def test_sort():
    frame = pd.DataFrame({'customer_id': [2, 1], 'timestamp': [2, 1], 'amount': [5, 7]})
    assert pd_sort_transactions(frame)['customer_id'].tolist() == [1, 2]
