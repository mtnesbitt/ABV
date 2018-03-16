from beer import Beer

def test_name():
    b = Beer("Guinness", "12/12 OZ. BTL", "Stout", "30.00")
    assert b.get_name() == "Guinness"
    assert b.get_size() == "12/12 OZ. BTL"
    assert b.get_style() == "Stout"
    assert b.get_price() == "30.00"
