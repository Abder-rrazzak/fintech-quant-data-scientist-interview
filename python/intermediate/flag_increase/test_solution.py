from solution import flag_increase

def test_flag():
    assert flag_increase(100, 160, 0.5) is True
    assert flag_increase(100, 140, 0.5) is False
