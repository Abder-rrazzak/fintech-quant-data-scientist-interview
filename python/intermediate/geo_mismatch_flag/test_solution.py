from solution import geo_mismatch_flag

def test_geo():
    assert geo_mismatch_flag('US', 'BR') == 1
    assert geo_mismatch_flag(None, 'US') == 0
