from solution import shared_customers

def test_shared():
    assert shared_customers([1, 2, 2], [2, 3]) == [2]
