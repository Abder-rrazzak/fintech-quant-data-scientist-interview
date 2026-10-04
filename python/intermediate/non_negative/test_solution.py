from solution import non_negative

def test_decorator():
    @non_negative
    def identity(value):
        return value
    assert identity(3) == 3
    try:
        identity(-1)
        raise AssertionError('expected')
    except ValueError:
        pass
