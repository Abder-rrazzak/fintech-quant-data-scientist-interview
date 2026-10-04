import pandas as pd
from solution import pd_drop_duplicate_ids

def test_drop_dup():
    frame = pd.DataFrame({'transaction_id': [1, 1, 2], 'amount': [3, 8, 1]})
    assert pd_drop_duplicate_ids(frame)['amount'].tolist() == [3, 1]
