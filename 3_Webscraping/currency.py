class Currency():
    def __init__(self, value, currency):
        self.value = value
        self.currency = currency
    
    def get_info(self):
        return f'{self.value} {self.currency}'