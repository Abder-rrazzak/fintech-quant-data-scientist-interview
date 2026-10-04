from solution import pairwise_stream

def test_pairs():
    assert list(pairwise_stream([1, 3, 6])) == [(1, 3), (3, 6)]
