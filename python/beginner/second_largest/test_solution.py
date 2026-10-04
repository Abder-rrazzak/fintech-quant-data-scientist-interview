from solution import second_largest

def test_second():
    assert second_largest([5, 5, 3, 9]) == 5
    assert second_largest([4, 4]) is None
