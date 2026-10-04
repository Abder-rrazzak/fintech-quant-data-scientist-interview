import pandas as pd
from solution import pd_customer_totals

def test_tot():
    frame = pd.DataFrame({'customer_id': [1, 1, 2], 'amount': [10.0, 5.0, 3.0]})
    result = pd_customer_totals(frame)
    assert result.loc[1] == 15.0 and result.loc[2] == 3.0
