from solution import take_first

def test_take():
    assert take_first(iter([1, 2, 3, 4]), 2) == [1, 2]
