import numpy as np
from solution import np_standardize_columns

def test_std():
    out = np_standardize_columns(np.array([[1.0, 5.0], [3.0, 5.0]]))
    assert abs(out[:, 0].mean()) < 1e-9
    assert out[:, 1].tolist() == [0.0, 0.0]
