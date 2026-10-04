import numpy as np
from solution import np_rate

def test_rate():
    assert np_rate(np.array([1, 0, 0, 1])) == 0.5
    assert np_rate(np.array([])) == 0.0
