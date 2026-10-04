from solution import new_customers

def test_new():
    assert new_customers([1, 2], [2, 3, 4]) == [3, 4]
