import numpy as np
from solution import np_threshold_flags

def test_flags():
    assert np_threshold_flags(np.array([0.2, 0.8]), 0.5).tolist() == [0, 1]
