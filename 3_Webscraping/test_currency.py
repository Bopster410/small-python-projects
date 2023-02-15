import currency

def test_multiplication():
    five = currency.Dollar(5)
    product = five.times(3)
    assert product.amount == 15
    product = five.times(4)
    assert product.amount== 20

def test_equals():
    assert currency.Dollar(5) == currency.Dollar(5)
    assert currency.Dollar(5) != currency.Dollar(6)