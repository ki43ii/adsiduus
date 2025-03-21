from ast import literal_eval
from random import randint

savefile = open("savefile.txt", "r")
previous_save = savefile.read()
previous_save = literal_eval(previous_save)

current_level = previous_save.get("level")
current_xp = previous_save.get("xp")

savefile = open("savefile.txt", "w")

# (Attack, Defense)
stats = {"barbarian" : (50, 50, 200, "rip"), "tank" : (20, 80, 400, "invincible"),
         "healer" : (30, 30, 300, "heal"), "warrior" : (80, 20, 150, "enrage")}

weapons = {"barbarian" : ("short-range knife", "hatchet", "rope", "mace",
                          "axe", "whip", "throwable axe", "scythe", "javelin"),

           "tank" : ("hands", "bow and arrow", "slab of iron", "crossbow", "shield",
                     "spiked shield", "titanium knuckles", "pistol", "a literal sniper rifle (lol)"),

           "healer" : ("safety scissors", "stethoscope", "reflex hammer", "cutting knife", "razer",
                       "textbook of Dermatology", "lancet (tests blood sugar)", "thermometer", "obsidian scalpel"),

           "warrior" : ("hands", "shortsword", "bow and arrow", "katana", "spiked shield",
                        "spinny spiky spoon", "crossbow", "dual-wield katana", "pistol")}

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

        self.level = current_level
        self.xp = current_xp
        # dividing by 5 to avoid overpowering level 9 players
        self.attack_strength = stats.get(playertype)[0] * self.level // 5  
        self.defense = stats.get(playertype)[1] * self.level // 5
        self.health = stats.get(playertype)[2] * self.level // 5
        self.special_move = stats.get(playertype)[3] * self.level // 5

    def levelup(self):

        self.xp = 0
        self.level += 1

        savefile.write(f"\{\"level\" : {self.level}, \"xp\" : {self.xp}}")

    def attack(self, enemy):
        
        pass
