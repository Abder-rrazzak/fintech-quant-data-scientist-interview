import numpy as np
from solution import np_unique_counts

def test_unique():
    values, counts = np_unique_counts(np.array([2, 1, 2]))
    assert values.tolist() == [1, 2] and counts.tolist() == [1, 2]
