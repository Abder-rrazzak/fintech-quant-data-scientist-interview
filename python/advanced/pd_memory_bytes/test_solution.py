import pandas as pd
from solution import pd_memory_bytes

def test_mem():
    frame = pd.DataFrame({'amount': [1.0, 2.0]})
    assert pd_memory_bytes(frame) > 0
