class Money():
    def __init__(self, amount):
        self._amount = amount

    def __eq__(self, __o: object) -> bool:
        return __o._amount == self._amount

class Dollar(Money):
    def times(self, multiplier) -> object:
        return Dollar(self._amount * multiplier)

class Ruble(Money):
    def times(self, multiplier) -> object:
        return Dollar(self._amount * multiplier)