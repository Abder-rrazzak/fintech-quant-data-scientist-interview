import numpy as np
from solution import np_float32_amounts

def test_f32():
    out = np_float32_amounts(np.array([1.5, 2.5]))
    assert out.dtype == np.float32
    assert out.tolist() == [1.5, 2.5]
