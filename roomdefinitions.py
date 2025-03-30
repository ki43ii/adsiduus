from playerclass import Enemy, Player
from collections import Counter
<<<<<<< HEAD
from random import choice, randint
from time import sleep
=======
from random import choice
import time
>>>>>>> 521dafc03559f13585192f09268c508df185dd62

# this will be useful in the allattack method
def format_enemyarray(arr):
    enemy_counts = Counter(arr)
    sorted_enemy_counts = sorted(enemy_counts.items(), key=lambda item: item[1], reverse=True)  # sorts by count descending
    
    formatted_result = []
    for enemy, count in sorted_enemy_counts:
        if enemy == sorted_enemy_counts[-1]:
            formatted_result.append(f"and {number_encoding.get(count)} {enemy}{"s" if count > 1 else ""}")

        else:
            formatted_result.append(f"{number_encoding.get(count)} {enemy}{"s" if count > 1 else ""}")
    
    return formatted_result

number_encoding = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve",
                   13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty"}

class DungeonRoom:

    def __init__(self, enemycount, difficulty):
        
        difficulty *= 10
        self.contained_enemies = []
        for i in range(enemycount):
            self.contained_enemies.append(Enemy(difficulty))

    # this will be useful in the allattack method
    def format_enemyarray(self, arr):
        enemy_counts = Counter(arr)
        sorted_enemy_counts = sorted(enemy_counts.items(), key=lambda item: item[1], reverse=True)  # sorts by count descending

        formatted_result = []
        for enemy, count in sorted_enemy_counts:
            if enemy == sorted_enemy_counts[-1]:
                formatted_result.append(f"and {number_encoding.get(count)} {enemy}{"s" if count > 1 else ""}")

            else:
                formatted_result.append(f"{number_encoding.get(count)} {enemy}{"s" if count > 1 else ""}")

        return formatted_result

    def allattack_player(self, player):

        hitters, missers = [], []
        hitenemies, missenemies = [], []
        
        totaldamagehit, totaldamagemissed = 0, 0

        for enemy in self.contained_enemies:
            attackvalues = enemy.attack(player, attackmode="dungeon")
            
            if attackvalues[2] == 1:  # it returns 1 if there is a hit or 0 if there isn't
                hitters.append(attackvalues)
            else:
                missers.append(attackvalues)

        for hit in hitters:
            
            hitenemies.append(hit[0])
            totaldamagehit += hit[1]

            player.health -= hit[1]

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

        print(f"""Lucky you! You have managed to dodge {totaldamagemissed} hit points worth of damage from {missenemiesstr}.""")
        if totaldamagehit > 0:
            print(f"""However, you were unable to avoid {totaldamagehit} hit points worth of damage from {hitenemiesstr}.

            You are left with {player.health} hit points after the attack.""")

    def allattack_eachother(self):

        pass

    def loot_dungeon(self):

        pass

class TripleDoorRoom:

    def __init__(self, difficulty, player):  # this should be given as a number 1-2

        self.difficulty = difficulty

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
<<<<<<< HEAD
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

                    attackcheck = input(f"You try to use option {attackcheck}, but you realise that it's not an actual option. Please respond with just the letter (a or b).\n\n")

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

class CheeseRoom:

	def __init__(self, difficulty):  # difficulty is 1, 2 or 3

		self.difficulty = difficulty
        self.enemy = Enemy(difficulty)

		print("You find yourself face to face with a broken yellow door and a gun on the floor. You try to look through but its completely dark, you look down and see what seems to be a rolled up letter, you bend over to pick it up...")
		
        sleep(2)

        before_time = time()                                                                                        
        decision = input("""But -- BANG, something explodes and you don't know what. Your vision is blurred; you look up and barely make out a tall figure henched over, ready to attack you.

                a) Shoot at it
                b) Run away.                                                                                                            c) Run at it.""")

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

                    if attackdec == "a":
                        player.attack(enemy)
                    else:
                        print("Strange choice, but alright.")

                elif decision == "c":
	   
		            print("That was not the smartest of ideas.")
                    enemy.attack(player)
