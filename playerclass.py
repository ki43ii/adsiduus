from random import randint

stats = {"barbarian" : (50, 50), "tank" : (20, 80), "healer" : (30, 30), "warrior" : (80, 20)}

enemytypes = {10: "dog", 20: "wolf", 30: "guard", 40: "armed guard", 50: "lead guard",
              60: "wizard", 70: "enraged wizard", 80: "high wizard", 90: "grand sorcerer",
              100: "tarrasque"}

class Enemy:

    def __init__(self, enemypower: int):  # here we define the enemy's stats based on its power

        if enemypower == 0:
            
            self.attack_strength = randint(10, 50)
            self.defense = randint(10, 50)
            self.health = randint(40, 120)

        if enemypower == 1:

            self.attack_strength = randint(25, 65)
            self.defense = randint(25, 65)
            self.health = randint(60, 180)

        elif enemypower == 2:
            
            self.attack_strength = randint(40, 80)
            self.defense = randint(40, 80)
            self.health = randint(120, 250)

        else:

            self.attack_strength = randint(60, 120)
            self.defense = randint(60, 120)
            self.health = randint(150, 300)

    def identify_type(self):  # this method identifies the enemy's type.
        
        stats_mean = self.attack_strength + self.defense + (self.health / 4) // 3  # mean of stats
        
        if stats_mean % 10 < 5: relative_power = "weak"
        else: relative_power = "powerful"

        return relative_power + enemytypes.get(round(stats_mean), -1)  # Rounded to tens place, put into dict at top.

class Player:

    def __init__(self, playertype):

        self.attack_strength = stats.get(playertype)[0]
        self.defense = stats.get(playertype)[1]
        self.health = 200

    def attack(self, enemy):
        
        pass
