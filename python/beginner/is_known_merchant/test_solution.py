from solution import is_known_merchant

def test_known():
    assert is_known_merchant({1, 2}, [1, 1]) is True
    assert is_known_merchant({1}, [2]) is False
