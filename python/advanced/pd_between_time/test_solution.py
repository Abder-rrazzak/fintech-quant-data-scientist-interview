import pandas as pd
from solution import pd_between_time

def test_between():
    frame = pd.DataFrame({'timestamp': ['2024-01-01', '2024-06-01'], 'amount': [1, 2]})
    out = pd_between_time(frame, '2024-01-01', '2024-03-01')
    assert out['amount'].tolist() == [1]
