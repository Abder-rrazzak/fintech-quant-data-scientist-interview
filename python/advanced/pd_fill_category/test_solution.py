import pandas as pd
from solution import pd_fill_category

def test_fill():
    frame = pd.DataFrame({'merchant_category': ['grocery', None]})
    assert pd_fill_category(frame)['merchant_category'].tolist() == ['grocery', 'unknown']
