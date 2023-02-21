class Money():
    def __init__(self, currency, amount=0):
        self._amount = amount
        self._currency = currency

    def __eq__(self, __o: object) -> bool:
        return __o._amount == self._amount and self.currency() == __o.currency()
    
    def __add__(self, __o: object):
        return Money(self.currency(), self._amount + __o._amount)
    
    def __str__(self) -> str:
        return f"{self._amount} {self._currency}"
    
    def __repr__(self) -> str:
        return self.__str__()

    def currency(self):
        return self._currency
    
    def dollar(self):
        return Money("USD", self._amount)
    
    def ruble(self):
        return Money("RUB", self._amount)

    def times(self, multiplier):
        return Money(self._currency, self._amount * multiplier)

