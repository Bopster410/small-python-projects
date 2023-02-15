import currency

def test_multiplication():
    five = currency.Dollar(5)
    product = five.times(3)
    assert product.amount == 15
    product = five.times(4)
    assert product.amount== 20