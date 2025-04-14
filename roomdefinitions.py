from playerclass import Enemy, Player
from collections import Counter
from random import choice, randint
from time import *

number_encoding = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve",
                   13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty"}

class DungeonRoom:

    def __init__(self, enemycount, difficulty, player):

        print(f"You find yourself in a dungeon room, trapped with {enemycount} angry enemies.")
        
        self.contained_enemies = []
        self.enemycount = enemycount
        self.invincible = 0
        self.move_used = 0
        player.cur_room = "dungeon"

        for _ in range(enemycount):
            self.contained_enemies.append(Enemy(10))
        
        while self.contained_enemies:
            attackdec = input(f"""What will you do next?
        a) Attack as many enemies as you can.
        b) Use your special move -- {player.special_move}.
        c) Sit there and watch, horrified.\n\n""")

            while attackdec not in ["a", "b", "c"] or (attackdec == "b" and self.move_used == 1):
                
                if attackdec not in ["a", "b", "c"]:
                    attackdec = input(f"You try to do option {attackdec}, but that's not an option. Please respond with a, b, or c: ")
                
                elif attackdec == "b" and self.move_used == 1:
                    attackdec = input("You are still panting from your special move. You can only choose a or c now: ")
            
            if attackdec == "a":
            
                print("You attack the closest five enemies to you. Here is what you manage.")
                
                for enemy in self.contained_enemies[-5:]:
                    player.attack(enemy)
                
                    if enemy.health <= 0:
                        self.contained_enemies.remove(enemy)
                
                self.contained_enemies = [e for e in self.contained_enemies if e.health > 0]  # cleaning up dead enemies

                print("\n" * 5 + "The tension builds. Suddenly, the enemies all attack.")
                
                if randint(1, 2) == 1:
                    self.allattack_player(player)
                
                else:
                    print("However!")
                    self.allattack_eachother()
            
            elif attackdec == "b":
            
                if player.special_move == "heal":
                
                    player.health += 1000
                    print(f"You feel a surge of relief. Your health increases by 1000 to {player.health} hit points.")
                
                elif player.special_move in ["rip", "enrage"]:
                
                    print("Rage surges through you. The thought of these monsters continuing to exist fuels your wrath... BANG!\n")
                    sleep(5)
                    dead_enemies = []
                    
                    for enemy in self.contained_enemies[1:]:
                        player.attack(enemy, player.weak_attack_strength)
                    
                        if enemy.health <= 0:
                            dead_enemies.append(enemy)
                    
                    self.contained_enemies = [x for x in self.contained_enemies if x not in dead_enemies]
                    
                    if self.contained_enemies:
                        print(f"Only a {self.contained_enemies[0].identify_type()} escapes. It runs away from the dungeon.\n")
                        self.contained_enemies.pop(0)
                
                if player.special_move == "invincible":
                    self.invincible = 1
                
                print("Immediately, every monster attacks you simultaneously.\n")
                sleep(3)
                self.allattack_player(player)
                self.move_used = 1
            
            elif attackdec == "c":
                print("You watch as the monsters confer and then scream: 'ATTACK!'\n")
                sleep(3)
            
                if randint(1, 3) == 1:
                    self.allattack_player(player)
                
                else:
                    print("However...")
                    self.allattack_eachother()
        
        self.loot_dungeon(player)

    def format_enemyarray(self, arr):
        
        counts = Counter(arr)
        sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
        result = []
        
        for i, (enemy, count) in enumerate(sorted_counts):
            prefix = "and " if i > 0 else ""
            result.append(f"{prefix}{number_encoding.get(count)} {enemy}s" if count > 1 else f"{prefix}a {enemy}")
        
        return result

    def allattack_player(self, player):
        
        hitters, missers = [], []
        hitenemies, missenemies = [], []
        totaldamagehit, totaldamagemissed = 0, 0
        
        for enemy in self.contained_enemies:
            
            attackvalues = enemy.attack(player, attackmode="dungeon")
        
            if attackvalues[2] == 1 and self.invincible == 0:
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
        
        hitenemies = self.format_enemyarray(hitenemies)
        missenemies = self.format_enemyarray(missenemies)
        
        if missenemies:
            mstr = ", ".join(missenemies)
            print(f"You manage to dodge {totaldamagemissed} hit points of damage from {mstr}.")
        
        if hitenemies:
            hstr = ", ".join(hitenemies)
            print(f"However, you take {totaldamagehit} hit points of damage from {hstr}. You now have {player.health} hit points.")

    def allattack_eachother(self):
        print("Confused, every enemy in the dungeon attacks another.\n")
        sleep(3)
        dead = []
        for cur_enemy in self.contained_enemies:
            hit = randint(0, 100) < 65
            targets = [e for e in self.contained_enemies if e != cur_enemy]
            if not targets:
                continue
            attacked_enemy = choice(targets)
            ca = "an" if cur_enemy.identify_type()[0] in "aeiou" else "a"
            aa = "an" if attacked_enemy.identify_type()[0] in "aeiou" else "a"
            attack = cur_enemy.attack(attacked_enemy, "dungeon")
            dmg = attack[1]
            if hit:
                attacked_enemy.health -= dmg
                print(f"{ca.upper()} {cur_enemy.identify_type()} attacks {aa} {attacked_enemy.identify_type()} for {dmg} damage, leaving it at {attacked_enemy.health}")
                if attacked_enemy.health <= 0:
                    attacked_enemy.dead()
                    dead.append(attacked_enemy)
            else:
                print(f"{ca.upper()} {cur_enemy.identify_type()} misses {aa} {attacked_enemy.identify_type()} (would have dealt {dmg} damage)")
        self.contained_enemies = [e for e in self.contained_enemies if e.health >= 0]

    def loot_dungeon(self, player):
        loot = choice(["a potion of healing.", "a potion of healing.", "a potion of healing.", "a potion of healing.",
                       "absolutely nothing.", "a genie with one wish.", "a one-time revive pass.", "a one-time revive pass."])
        print(f"After defeating all enemies, you find a chest containing {loot}")
        if loot == "a potion of healing.":
            player.health += 200
            print(f"You use the potion and gain 200 hit points, now at {player.health} hit points.\n\n")
        if loot == "a genie with one wish.":
            input("The genie asks: 'What is your wish? (no wishing for more wishes)'\n")
            print("\n\nYou wait excitedly. The genie speaks confidently.")
            sleep(1)
            print("\n\"I don't care.\"\n\n")
        if loot == "a one-time revive pass.":
            print("Your next death won't lose any progress.\n\n")

        sleep(4)


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

        decision = input("""But -- BANG, something explodes and you don't know what. Your vision is blurred; you look up and barely make out a tall figure henched over, ready to attack you.

                a) Shoot at it
                b) Run away.
                c) Run at it.\n\n""").lower()

        while True:

            if decision == "a":

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
