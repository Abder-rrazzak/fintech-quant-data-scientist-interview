from solution import max_amount

def test_max():
    assert max_amount([3.0, 9.0, 4.0]) == 9.0
    try:
        max_amount([])
        raise AssertionError('expected')
    except ValueError:
        pass
