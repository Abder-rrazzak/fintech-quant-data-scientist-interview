import numpy as np
from solution import np_draw_mask

def test_draw():
    first = np_draw_mask(5, 1)
    second = np_draw_mask(5, 1)
    assert first.tolist() == second.tolist()
    assert len(first) == 5
