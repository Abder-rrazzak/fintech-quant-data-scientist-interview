from solution import pairwise_diffs

def test_diffs():
    assert pairwise_diffs([10, 12, 9]) == [2, -3]
    assert pairwise_diffs([4]) == []
