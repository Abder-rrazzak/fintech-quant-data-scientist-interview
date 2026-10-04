from solution import high_risk_mcc

def test_mcc():
    assert high_risk_mcc('crypto') == 1
    assert high_risk_mcc('grocery') == 0
