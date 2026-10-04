import pandas as pd
from solution import pd_merge_customers

def test_merge():
    tx = pd.DataFrame({'customer_id': [1], 'amount': [5]})
    cust = pd.DataFrame({'customer_id': [1], 'country': ['US']})
    out = pd_merge_customers(tx, cust)
    assert out.loc[0, 'country'] == 'US'
