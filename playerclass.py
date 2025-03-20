
stats = {"barbarian" : (50, 50), "tank" : (20, 80), "healer" : (30, 30), "warrior" : (80, 20)}

class Player:

    def __init__(self, playertype):

        self.attack_strength = stats.get(playertype)[0]
        self.defense = stats.get(playertype)[1]
