from random import randint

stats = {"barbarian" : (50, 50), "tank" : (20, 80), "healer" : (30, 30), "warrior" : (80, 20)}

class Enemy:

    def __init__(self, enemytype):

        self.attack_strength = randint(10, 100)
        self.defense = randint(10, 100)
        self.health = randint(75, 175)

    def identify_type(self):

        pass

class Player:

    def __init__(self, playertype):

        self.attack_strength = stats.get(playertype)[0]
        self.defense = stats.get(playertype)[1]
        self.health = 200

    def attack(self, enemy):
        
        pass
