from solution import group_sum

def test_group():
    assert group_sum([(1, 2.0), (2, 3.0), (1, 4.0)]) == {1: 6.0, 2: 3.0}
