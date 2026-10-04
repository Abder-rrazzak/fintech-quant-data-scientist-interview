from solution import expected_loss_identity

def test_el():
    assert abs(expected_loss_identity(0.02, 0.45, 10000) - 90.0) < 1e-6
