import pandas as pd
from solution import pd_join_indicator

def test_ind():
    left = pd.DataFrame({'customer_id': [1]})
    right = pd.DataFrame({'customer_id': [1, 2]})
    counts = pd_join_indicator(left, right)
    assert counts['both'] == 1 and counts['right_only'] == 1
