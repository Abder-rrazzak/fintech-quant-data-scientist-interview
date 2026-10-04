import pandas as pd
from solution import pd_pivot_month

def test_pivot():
    frame = pd.DataFrame({'customer_id': [1, 1], 'month': ['2024-01', '2024-02'], 'amount': [2.0, 3.0]})
    out = pd_pivot_month(frame)
    assert out.loc[1, '2024-01'] == 2.0
