import numpy as np
from solution import np_safe_divide

def test_div():
    out = np_safe_divide(np.array([1.0, 1.0]), np.array([2.0, 0.0]), fill=-1)
    assert out.tolist() == [0.5, -1.0]
