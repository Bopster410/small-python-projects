import currency

def test_multiplication():
    five = currency.Dollar(5)
    five.times(3)
    assert five.amount == 15