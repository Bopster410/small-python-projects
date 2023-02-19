class Money():
    def __init__(self, currency, amount=0):
        self._amount = amount
        self._currency = currency

    def __eq__(self, __o: object) -> bool:
        return __o._amount == self._amount and type(self) == type(__o)

    def currency(self):
        return self._currency
    
    def dollar(self):
        return Dollar("USD", self._amount)
    
    def ruble(self):
        return Ruble("RUB", self._amount)


class Dollar(Money):
    def __init__(self, currency, amount=0):
        super().__init__(currency, amount)

    def times(self, multiplier) -> Money:
        return Money(self._currency, self._amount * multiplier).dollar()
    

class Ruble(Money):
    def __init__(self, currency, amount=0):
        super().__init__(currency, amount)
        
    def times(self, multiplier) -> Money:
        return Money(self._currency, self._amount * multiplier).ruble()
