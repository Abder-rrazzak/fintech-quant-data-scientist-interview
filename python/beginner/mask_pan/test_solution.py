from solution import mask_pan

def test_mask():
    assert mask_pan('4111111111111111') == '************1111'
    assert mask_pan('1234') == '1234'
