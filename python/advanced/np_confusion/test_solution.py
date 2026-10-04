import numpy as np
from solution import np_confusion

def test_cm():
    assert np_confusion(np.array([1, 0, 1, 0]), np.array([1, 1, 0, 0])) == (1, 1, 1, 1)
