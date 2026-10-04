import pandas as pd
from solution import pd_group_size

def test_size():
    frame = pd.DataFrame({'customer_id': [1, 1, 2]})
    assert pd_group_size(frame).loc[1] == 2
