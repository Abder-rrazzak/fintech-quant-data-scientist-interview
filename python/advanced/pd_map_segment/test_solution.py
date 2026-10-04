import pandas as pd
from solution import pd_map_segment

def test_map():
    frame = pd.DataFrame({'customer_segment': ['a', 'z']})
    out = pd_map_segment(frame, {'a': 'retail'})
    assert out['segment_name'].tolist() == ['retail', 'other']
