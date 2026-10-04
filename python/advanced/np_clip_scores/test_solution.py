import numpy as np
from solution import np_clip_scores

def test_clip():
    assert np_clip_scores(np.array([-0.2, 0.4, 1.3])).tolist() == [0.0, 0.4, 1.0]
