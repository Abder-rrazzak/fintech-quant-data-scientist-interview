from solution import dedupe_preserve_order

def test_dedupe():
    assert dedupe_preserve_order([3, 1, 3, 2, 1]) == [3, 1, 2]
