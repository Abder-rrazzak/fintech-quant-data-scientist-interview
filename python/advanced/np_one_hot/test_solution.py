import numpy as np
from solution import np_one_hot

def test_hot():
    out = np_one_hot(np.array([0, 2]), 3)
    assert out.tolist() == [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
