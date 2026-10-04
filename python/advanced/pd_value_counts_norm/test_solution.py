import pandas as pd
from solution import pd_value_counts_norm

def test_vc():
    frame = pd.DataFrame({'merchant_category': ['a', 'a', 'b', 'b']})
    out = pd_value_counts_norm(frame)
    assert out.loc['a'] == 0.5
