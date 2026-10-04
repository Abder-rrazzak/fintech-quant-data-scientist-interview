from solution import require_currency

def test_require():
    assert require_currency('EUR') == 'EUR'
    try:
        require_currency('JPY')
        raise AssertionError('expected')
    except ValueError:
        pass
