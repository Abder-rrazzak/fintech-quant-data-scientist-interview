import numpy as np
from solution import np_log1p_clip

def test_log():
    out = np_log1p_clip(np.array([0.0, -4.0]))
    assert out.tolist() == [0.0, 0.0]
