import pandas as pd
from solution import pd_concat_days

def test_concat():
    a = pd.DataFrame({'amount': [1]})
    b = pd.DataFrame({'amount': [2]})
    assert pd_concat_days([a, b])['amount'].tolist() == [1, 2]
