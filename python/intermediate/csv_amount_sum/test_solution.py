from solution import csv_amount_sum

def test_csv():
    assert csv_amount_sum('id,amount\n1,2.5\n2,3\n') == 5.5
