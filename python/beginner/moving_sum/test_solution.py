from solution import moving_sum

def test_moving():
    assert moving_sum([1, 2, 3, 4], 2) == [3, 5, 7]
    assert moving_sum([1, 2], 5) == []
