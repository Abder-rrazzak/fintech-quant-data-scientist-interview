from solution import filter_large

def test_filter():
    assert filter_large({1: 10.0, 2: 3.0}, 5) == {1: 10.0}
