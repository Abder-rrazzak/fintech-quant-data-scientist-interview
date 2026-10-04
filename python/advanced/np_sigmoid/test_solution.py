import numpy as np
from solution import np_sigmoid

def test_sig():
    assert np_sigmoid(np.array([0.0]))[0] == 0.5
