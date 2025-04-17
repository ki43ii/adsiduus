from time import sleep
from random import randint

enemytypes = {0: "dog", 10: "wolf", 20: "goblin", 30: "guard", 40: "armed guard", 50: "lead guard",
              60: "wizard", 70: "enraged wizard", 80: "high wizard", 90: "grand sorcerer",
              100: "tarrasque"}

class Enemy:

    def __init__(self, enemypower: int):  # here we define the enemy's stats based on its power

        self.enemypower = enemypower
        if enemypower == 0:
            
            self.attack_strength = randint(10, 50)
            self.defense = randint(10, 50)
            self.health = randint(40, 120)
            self.hit_chance = 60

        if enemypower == 1:

            self.attack_strength = randint(25, 65)
            self.defense = randint(25, 65)
            self.health = randint(60, 180)
            self.hit_chance = 70

        elif enemypower == 2:

            self.attack_strength = randint(40, 80)
            self.defense = randint(40, 80)
            self.health = randint(120, 250)
            self.hit_chance = 80

        elif enemypower == 10:  # 10 encodes a trivial enemy that can be beaten almost instantly

            self.attack_strength = randint(5, 30)
            self.defense = randint(15, 30)
            self.health = randint(15, 30)
            self.hit_chance = 7

        else:

            self.attack_strength = randint(60, 120)
            self.defense = randint(60, 120)
            self.health = randint(150, 300)
            self.hit_chance = 90

    def identify_type(self):  # this method identifies the enemy's type.
        
        stats_mean = (self.attack_strength + self.defense + self.health / 4) // 3  # mean of stats
        
        if stats_mean % 10 < 5: relative_power = "weak"
        else: relative_power = "powerful"
        
        return f"{relative_power} {enemytypes.get(round(stats_mean, -1))}"  # Rounded to tens place, put into dict at top.

    def damage(self, attacker, dmg):  # attacker parameter unnecessary
        self.health -= dmg

    def attack(self, target, attackmode = None):

        possible_damage = self.attack_strength * 50 // target.defense # roughly 50 is average defense stat
        
        if randint(0, 100) <= self.hit_chance:

            if attackmode == "dungeon":  # exception for dungeon rooms, explained in roomdefinitions.py
                return (self.identify_type(), possible_damage, 1)
            
            else:
                target.damage(self, possible_damage)

                print(f"""You have been hit by the {self.identify_type()}. It dealt {str(possible_damage)} damage to you.
                  You are left with {target.health} hit points.""")
        
        else:
            if attackmode == "dungeon":
                return (self.identify_type(), possible_damage, 0)
            else:
                print(f"""Lucky you! The {self.identify_type()} has missed its attack on you.
                You would have taken {possible_damage} hit points of damage.""")

    def dead(self):
        print(f"The {self.identify_type()} dies.")

    def dead_byplayer(self, player):

        print(f"You have taken out the {self.identify_type()} with {player.health} hit points remaining.")

        if self.enemypower < 5: xpgained = self.enemypower
        elif self.enemypower < 50: xpgained = self.enemypower // 10
        else: xpgained = self.enemypower // 100

        player.xp += xpgained
        print(f"You gain {xpgained} xp.")

        player.levelup()

# player attack and defense stats based on class
stats = {"barbarian" : (100, 50, 300, "rip"), "tank" : (40, 80, 500, "invincible"),
         "healer" : (60, 30, 400, "heal"), "warrior" : (150, 20, 350, "enrage")}

# weapon for each level for each player class
weapons = {"barbarian" : ("short-range knife", "hatchet", "rope", "mace",
                          "axe", "whip", "throwable axe", "scythe", "javelin"),

           "tank" : ("hands", "bow and arrow", "slab of iron", "crossbow", "shield",
                     "spiked shield", "titanium knuckles", "pistol", "a literal sniper rifle (lol)"),

           "healer" : ("safety scissors", "stethoscope", "reflex hammer", "cutting knife", "razer",
                       "textbook of Dermatology", "lancet (tests blood sugar)", "thermometer", "obsidian scalpel"),

           "warrior" : ("hands", "shortsword", "bow and arrow", "katana", "spiked shield",
                        "spinny spiky spoon", "crossbow", "dual-wield katana", "pistol")}

def save(p, savefile):
    with open(savefile, "w") as savefile:
        savefile.write("{" + f"'level' : {p.level}, 'xp' : {p.xp}, 'playertype' : '{p.playertype}', 'health' : {p.health}, 'checkpoint' : '{p.cur_room}'" + "}")

class Player:

    def __init__(self, playertype, save_data, savefile):

        self.playertype = playertype
        self.savefile = savefile
        self.saveinfo = save_data
        self.cur_room = None
        self.cur_room_class = None
        self.level = self.saveinfo.get("level")
        self.xp = self.saveinfo.get("xp")
        # dividing by 5 to avoid overpowering high level players
        self.attack_strength = stats.get(playertype)[0] * self.level // 2
        self.weak_attack_strength = self.attack_strength // 7
        self.defense = stats.get(playertype)[1] // 2 + stats.get(playertype)[1] * self.level // 5
        if self.saveinfo.get("health") == None: self.health = stats.get(playertype)[2] // 2 + stats.get(playertype)[2] * self.level // 5
        else: self.health = self.saveinfo.get("health")
        self.hit_chance = 60 + stats.get(playertype)[0] * self.level // 40
        self.special_move = stats.get(playertype)[3]
        self.weapon = weapons.get(playertype)[self.level - 1]  # as levels are 1-indexed
        self.finalboss = 0
        self.save()
        
        print(f"Congratulations on beginning your adventure as a {playertype}.")
        print(f"You will begin your journey as a level 1 with your trusty {weapons.get(playertype)[self.level - 1]}.")
        print(f"You are granted an incredible power; your special move is {self.special_move}.")

        self.stats = f"""Here are your player's stats:

            Attack strength:        {self.attack_strength}
            Sweep attack strength:  {self.weak_attack_strength}  (Used during wide attacks)
            Defense:                {self.defense}
            Health:                 {self.health}
            Hit chance:             {self.hit_chance}
            Special move:           {self.special_move}
            Weapon:                 {self.weapon}

            Level:                  {self.level}
            Experience:             {self.xp}\n"""

    def levelup(self):

        if self.level <= 9:
            if self.xp >= 50:
                self.xp -= 50
                self.level += 1

                self.attack_strength = stats.get(self.playertype)[0] * self.level // 5
                self.defense = stats.get(self.playertype)[1] // 2 + stats.get(self.playertype)[1] * self.level // 5
                self.health = stats.get(self.playertype)[2] // 2 + stats.get(self.playertype)[2] * self.level // 5

                self.weapon = weapons.get(self.playertype)[self.level - 1]  # as levels are 1-indexed
                print(f"""Congratulations! You have leveled up. You are now level {self.level}. Your weapon has also been upgraded to a {self.weapon}.
                  You now deal a little bit more damage to enemies, and you can defend more attacks.

                  Remember, at any time, typing stats will give a list of your stats.\n\n""")
                self.save()
        else:
            self.finalboss = 1

    def damage(self, attacker, dealt_damage):  # note that the attacker parameter is not used

        self.health -= dealt_damage
        self.save()

    def save(self):
        save(self, self.savefile)

    def attack(self, target, attack_strength=None):
       
        if attack_strength == None: attack_strength = self.attack_strength  # no idea why i had to do this. python is dumb.

        possible_damage = attack_strength * 50 // target.defense # roughly 50 is average defense stat

        if randint(0, 100) <= self.hit_chance:
            
            target.health -= possible_damage

            print(f"""You attack the {target.identify_type()} with your {self.weapon}. You have dealt {str(possible_damage)} damage to it.
                  It is left with {target.health} hit points.""")
        
        if target.health <= 0:
            target.dead_byplayer(self)

    def dead(self):

        print("""Your vision blurs. You feel your heart slow down. Your fingers go numb, dropping your weapon.

        This is the end.""")
        sleep(2)

        print("""Through your foggy eyes, you see a dark wizard. You hear the terrible voice say to you:

        \033[31;1;0mYou lose...\033[0m""")

        sleep(3)
        print("Lucky for you, you have the revive pass.\n\n")

        print("You will start off again with 250 health.\n\n")

        self.health = 250
