import numpy as np
from solution import np_argmax_amount

def test_arg():
    assert np_argmax_amount(np.array([1.0, 4.0, 4.0, 2.0])) == 1
