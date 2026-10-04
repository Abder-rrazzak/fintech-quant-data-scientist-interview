from solution import invert_unique

def test_invert():
    assert invert_unique({'usd': 'US'}) == {'US': 'usd'}
    try:
        invert_unique({'a': 'x', 'b': 'x'})
        raise AssertionError('expected')
    except ValueError:
        pass
