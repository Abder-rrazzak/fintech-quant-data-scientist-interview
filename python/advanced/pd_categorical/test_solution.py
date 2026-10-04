import pandas as pd
from solution import pd_categorical

def test_cat():
    frame = pd.DataFrame({'merchant_category': ['grocery', 'fuel']})
    out = pd_categorical(frame, ['fuel', 'grocery'])
    assert str(out['merchant_category'].dtype) == 'category'
