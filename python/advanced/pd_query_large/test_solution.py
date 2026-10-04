import pandas as pd
from solution import pd_query_large

def test_q():
    frame = pd.DataFrame({'amount': [1.0, 5.0, 9.0]})
    assert pd_query_large(frame, 4)['amount'].tolist() == [5.0, 9.0]
