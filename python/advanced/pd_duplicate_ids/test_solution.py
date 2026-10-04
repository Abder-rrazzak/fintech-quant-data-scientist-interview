import pandas as pd
from solution import pd_duplicate_ids

def test_dup():
    frame = pd.DataFrame({'transaction_id': [1, 2, 1]})
    assert pd_duplicate_ids(frame) == [1]
