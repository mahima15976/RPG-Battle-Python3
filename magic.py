import random


class Spell:
    def __init__(self, name, cost, damage, type):
        self.name = name
        self. cost = cost
        self.damage = damage
        self.type = type

    def generate_damage(self):
        low = self.damage - 10
        high = self.damage + 10
        return random.randrange(low, high)