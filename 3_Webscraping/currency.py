class Money():
    def __init__(self, amount=0):
        self._amount = amount

    def __eq__(self, __o: object) -> bool:
        return __o._amount == self._amount and type(self) == type(__o)
    
    def dollar(self):
        return Dollar(self._amount)
    
    def ruble(self):
        return Ruble(self._amount)

class Dollar(Money):
    def times(self, multiplier) -> Money:
        return Dollar(self._amount * multiplier)

class Ruble(Money):
    def times(self, multiplier) -> Money:
        return Ruble(self._amount * multiplier)