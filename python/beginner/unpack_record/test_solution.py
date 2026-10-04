from solution import unpack_record

def test_unpack():
    assert unpack_record((7, 12.5, 'US')) == {'customer_id': 7, 'amount': 12.5, 'country': 'US'}
