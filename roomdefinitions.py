from playerclass import Enemy, Player
from collections import Counter
from random import choice, randint
from time import *

number_encoding = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve",
                   13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty"}

class DungeonRoom:

    def __init__(self, enemycount, difficulty, player):
        
        difficulty *= 10
        self.contained_enemies = []
        self.enemycount = enemycount
        self.invincible = 0
        self.move_used = 0
        player.cur_room = "dungeon"

        for i in range(enemycount):
            self.contained_enemies.append(Enemy(difficulty))

        attackdec = input(f"""You find yourself in a dungeon room. Trapped with you are {enemycount} different enemies. What will you do? Think fast.

              a) Attack as many enemies as you can.
              b) Use your special move -- {player.special_move}.
              c) Sit there and watch, horrified.\n\n""")

        while True:

            while True:
                if attackdec not in ["a", "b", "c"]:
                    attackdec = input(f"You try to do option {attackdec}, but you realise that's not an option. Please respond with just the letter: a, b or c?\n\n")
                elif attackdec == "b" and self.move_used == 1:
                    attackdec = input("You are still panting from the use of your special move before. You cannot use it again until after exiting this dungeon. You can only respond with the letters a or c now.\n\n")
                else: break
        
            if attackdec == "a":
                print("You attack the closest five enemies to you. Here is what you manage.")

                for enemy in self.contained_enemies[enemycount - 6:]:
                    player.attack(enemy)

                    if enemy.health <= 0:
                        self.contained_enemies.remove(enemy)

                print("\n" * 5 + "The tension builds in the room. The monsters' fury spreads like a wildfire. Suddenly: the enemies all go for an attack.")

                if randint(1,2) == 1:
                    self.allattack_player(player)
                else:
                    print("However!")
                    self.allattack_eachother()

            elif attackdec == "b":
            
                if player.special_move == "heal":
                    player.health += 1000
                    print(f"You feel a surge of relief and blood rushes through your veins. Your health increases by 1 000. You now have {player.health} hit points.")
                elif player.special_move == "rip" or player.special_move == "enrage":
                    print(f"Rage pumps through your veins. The pure thought of these monsters continuing to exist fuels your wrath. BANG!\n\n\n\n\n")
                    sleep(5)

                    dead_enemies = []
                    for enemy in self.contained_enemies[1:]:
                        player.attack(enemy, player.weak_attack_strength)  # weaker attack used for sweep attacks

                        if enemy.health <= 0:
                            dead_enemies.append(enemy)
                    self.contained_enemies = [x for x in self.contained_enemies if x not in dead_enemies]

                    print(f"Only a {self.contained_enemies[0].identify_type()} gets away unscathed. In fear, it runs away, exiting the dungeon.\n\n")
                    self.contained_enemies.pop(0)

                if player.special_move == "invincible": self.invincible = 1

                print("Immediately, every monster jumps up; they sprint forward and attack you simultaneously.\n\n\n\n\n")
                sleep(3)

                self.allattack_player(player)

                self.move_used = 1

            elif attackdec == "c":

                print("""You watch as the monsters consult, wondering what to do with you. 
                  Though you cannot make out most of their language, there is one word you do understand -- they all collectively scream:

                  'ATTACK!'\n\n\n\n""")

                sleep(3)

                if randint(1,3) == 1:
                    self.allattack_player(player)  # only 1/3 chance so that there's a bigger chance they don't immediately die for being stupid
                else:
                    print("However...")
                    self.allattack_eachother()

            if len(self.contained_enemies) == 0:
                break

            attackdec = input("You are given the same options as before. What will you do; a, b or c?\n\n")

        self.loot_dungeon(player)

    # this will be useful in the allattack method
    def format_enemyarray(self, arr):
        enemy_counts = Counter(arr)
        sorted_enemy_counts = sorted(enemy_counts.items(), key=lambda item: item[1], reverse=True)  # sorts by count descending

        formatted_result = []
        for enemy, count in sorted_enemy_counts:
            if enemy == sorted_enemy_counts[-1]:
                if count > 1: formatted_result.append(f"and {number_encoding.get(count)} {enemy}s")
                else: formatted_result.append(f"a {enemy}")

            else:
                if count > 1: formatted_result.append(f"and {number_encoding.get(count)} {enemy}s")
                else: formatted_result.append(f"a {enemy}")

        return formatted_result

    def allattack_player(self, player):

        hitters, missers = [], []
        hitenemies, missenemies = [], []
        
        totaldamagehit, totaldamagemissed = 0, 0

        for enemy in self.contained_enemies:
            attackvalues = enemy.attack(player, attackmode="dungeon")
            
            if attackvalues[2] == 1 and self.invincible == 0:  # it returns 1 if there is a hit or 0 if there isn't. if invincible, attack must miss.
                hitters.append(attackvalues)
            else:
                missers.append(attackvalues)

        for hit in hitters:
            
            hitenemies.append(hit[0])
            totaldamagehit += hit[1]

            player.damage(hit[0], hit[1])

        for miss in missers:

            missenemies.append(miss[0])
            totaldamagemissed += miss[1]

        hitenemies, missenemies = self.format_enemyarray(hitenemies), self.format_enemyarray(missenemies)

        if hitenemies:
            # converting hitenemies and missenemies to strings
            hitenemiesstr = hitenemies[0]
            for item in hitenemies[1:]: hitenemiesstr += f", {item}"
        
        missenemiesstr = missenemies[0]
        for item in missenemies[1:]: missenemiesstr += f", {item}"

        print(f"You manage to dodge {totaldamagemissed} hit points worth of damage from {missenemiesstr}.")
        if totaldamagehit > 0:
            print(f"""However, you were unable to avoid {totaldamagehit} hit points worth of damage from {hitenemiesstr}.

            You are left with {player.health} hit points after the attack.""")

    def allattack_eachother(self):  # requires PATCHING
        print("Confused, every enemy in the dungeon attacks another. This is how it goes down.\n\n\n\n\n")

        sleep(3)

        for enemy in range(len(self.contained_enemies)):
            
            if randint(0, 100) < 65: hit = 1
            else: hit = 0

            cur_enemy = self.contained_enemies[enemy]
            attacked_enemy = choice(self.contained_enemies)

            dead_enemies = []

            if cur_enemy.identify_type()[0] == "e": ca = "an"
            else: ca = "a"  # only enraged wizards start with a vowel
            
            if attacked_enemy.identify_type()[0] == "e": aa = "an"
            else: aa = "a"

            attack = cur_enemy.attack(attacked_enemy, "dungeon")  # every enemy attacks a random other enemy
            
            possible_dmg = attack[1]

            if hit == 1:
                attacked_enemy.health -= possible_dmg

                print(f"{ca.upper()} {cur_enemy.identify_type()} attacks {aa} {attacked_enemy.identify_type()} for {possible_dmg} hit points, leaving it on {attacked_enemy.health}")

                if attacked_enemy.health <= 0: 
                    attacked_enemy.dead()
                    dead_enemies.append(attacked_enemy)

            if hit == 0:
                print(f"{ca.upper()} {cur_enemy.identify_type()} misses an attack on {aa} {attacked_enemy.identify_type()} that would've dealt {possible_dmg} damage")

        self.contained_enemies = [x for x in self.contained_enemies if x not in dead_enemies]

    def loot_dungeon(self, player):

        loot = choice(["a potion of healing.", "a potion of healing.", "a potion of healing.", "a potion of healing.", "absolutely nothing.", "a genie with one wish.", "a one-time revive pass.", "a one-time revive pass."])
        print(f"After defeating all the enemies, you find a chest. You open it grandiosely -- and you are rewarded with {loot}")

        if loot == "a potion of healing.":
            player.health += 200
            print("You crack open the healing potion, and you get an increase of 200 to your health! You now have {player.health} hit points")

        if loot == "a genie with one wish.":
            input("The genie's voice reverberates through the room. \"What is your wish? (no wishing for more wishes)\"\n\n")
            print("The genie responds: \"I literally don't care\". He leaves.")

        if loot == "a one-time revive pass.":
            print("On your next death, you will not lose any progress.")


class TripleDoorRoom:

    def __init__(self, difficulty, player):  # this should be given as a number 1-2

        self.difficulty = difficulty
        player.cur_room = "three_door"

        roomchoice = input("""You stumble into a room with three doors. One door leads to you escaping completely unscathed. The other doors lead to traps; you don't yet know what they are, but you don't want to find out. You enter one of the following options on a piece of paper. Choose wisely.

        a) Go through door A.
        b) Go through door B.
        c) Go through door C.\n\n""")

        while True:
            
            if roomchoice not in ("a", "b", "c"):

                roomchoice = input("You enter your choice, but the paper comes right back. A message in blood is written on the wall: \"Just enter the letter. Nothing else\".\n\n")

            else:
                break

        self.choice = randint(1, 3)

        if self.choice == 1:
            self.strongenemy(difficulty, player)
        elif self.choice == 2:
            self.fakefreedom(difficulty, player)
        else:
            self.freedom()

    def strongenemy(self, difficulty, player):

        enemy = Enemy(difficulty)

        print(f"You find yourself stuck in a room. Your only companion? A -- clearly furious -- {enemy.identify_type()}.")

        while True:

            enemy.attack(player)

            if player.health <= 0:
                player.dead()
                break

            attackcheck = input(f"""\nShivering in fear, you realise your options. What will you do?

        a) Attack the {enemy.identify_type()}.
        b) Try to befriend it, such that it lets you pass.\n\n""")

            while True:

                if attackcheck not in ("a", "b"):
                    attackcheck = input(f"You try to do option {attackcheck}, but you realise that's not an option. The {enemy.identify_type()} approaches. You don't have much time. Respond with the option a or b, before it's too late.\n\n")

                else:
                    break

            if attackcheck == "a":
                player.attack(enemy)
            else:
                if randint(0,1) == 1:  # 50% chance of taming
                    print("It allows you to continue your journey unscathed. You thank it and continue through the door, exiting the room.")
                    break
                else:
                    print("It ignores you completely and continues its attack")

            if enemy.health <= 0:
                enemy.dead_byplayer(player)
                break


    def fakefreedom(self, difficulty, player):

        print("You see the light in front of you. You see that you have escaped.")
        sleep(1)

        player.health -= difficulty * 50
        print(f"As you exit, you feel a sharp pain in your foot. You have stepped on a pressure plate, and you are splashed by one of the Glitch's dark potions. You lose {difficulty * 50} health, leaving you with {player.health} hit points.")
        
        sleep(1)
        print("However, you do escape otherwise safe. You may now continue your journey.")

    def freedom(self):

        print("You see the light in front of you. You see that you have escaped.")

        sleep(1)

        print("You leave the room completely unscathed. You were lucky this time.")

class ShootRoom:  # this is a simple room. you are given the opportunity to shoot your enemy, or just do a normal attack. (or die)

    def __init__(self, difficulty, player):  # difficulty is 1, 2 or 3

        player.cur_room = "shoot_room"
        enemy = Enemy(difficulty)

        print("You find yourself face to face with a broken yellow door and a gun on the floor. You try to look through but its completely dark, you look down and see what seems to be a rolled up letter, you bend over to pick it up...")
		
        sleep(2)

        before_time = time()                                                                                        
        decision = input("""But -- BANG, something explodes and you don't know what. Your vision is blurred; you look up and barely make out a tall figure henched over, ready to attack you.

                a) Shoot at it
                b) Run away.
                c) Run at it.\n\n""").lower()

        while True:

            if time() - before_time > 20:

                print("Due to your inability to make decisions, the creature grabs onto you, ripping you apart while deriding your scream and cries for help")

            elif decision == "a":

                print("The creature falls, though you are still unable to make out what it is.")
                enemy.dead_byplayer(player)
                break

            elif decision == "b":

                print(f"The {enemy.identify_type()} catches up to you, ripping you slowly to bits with its sharp and jagged nails.")
                enemy.attack(player)

                attackdec = input(f"""Would you like to attack it back?

                        a) Yes.
                        b) No.\n\n""")

                if player.health <= 0:
                    player.dead()

                if attackdec == "a":
                    player.attack(enemy)
                    enemy.dead_byplayer(player)
                else:
                    print("Strange choice, but alright.")

            elif decision == "c":
	   
                print("That was not the smartest of ideas.")
                enemy.attack(player)

            decision = input("You have the same options as before. a, b, or c?\n\n")

class EmptyRoom:

    def __init__(self, player):

        self.q_ans = {}
        self.q = tuple(self.q_ans.keys())
        self.ans = tuple(self.q_ans.values())

        qnumber = randint(0,len(self.questions))

        print("""You step into an empty room. On the wall, you see a bloody inscription.

        \033[1;31m Would you like to play a game?

        The writing morphs.""")

        sleep(3)

        before_ans_time = time()
        answer = input(f"""\033[1;31m{self.q[qnumber]}

        You have 45 seconds.\n\n\n\n)""")
        
        while True:
            
            after_ans_time = time()

            if after_ans_time - before_ans_time >= 45:
                print("""It morphs again. 

        \033[1;31mToo late.                

Suddenly, you feel a horrible pain in your foot.

You take 50 damage.\n""")
                player.damage(50)
        
            elif answer != self.ans[qnumber]:

                answer = input("That isn't quite right. Make sure your input is spelt correctly if you forgot.\n\n")  # to be completed
