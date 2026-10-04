import pandas as pd
from solution import pd_month_key

def test_month():
    frame = pd.DataFrame({'timestamp': ['2024-03-02', '2024-11-01']})
    assert pd_month_key(frame).tolist() == ['2024-03', '2024-11']
