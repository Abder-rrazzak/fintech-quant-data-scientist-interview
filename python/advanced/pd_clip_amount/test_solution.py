import pandas as pd
from solution import pd_clip_amount

def test_clip():
    frame = pd.DataFrame({'amount': [-1.0, 5.0, 20.0]})
    assert pd_clip_amount(frame, 0, 10)['amount'].tolist() == [0.0, 5.0, 10.0]
