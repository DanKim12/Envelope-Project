import random

class Envelope:
    def __init__(self):
        self.amount = self.generate_amount()

    def generate_amount(self):
        return random.randint(1, 1000)

    def get_amount(self):
        return self.amount