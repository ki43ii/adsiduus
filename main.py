from playerclass import *
from roomdefinitions import *
from random import *
from sprites import *

playertype = input("""You will soon embark on your journey, fighting the horrible Glitch.
            A kind wizard appears next to you. He asks what class you would like to play.
        He gives you the following four options, and tells you to respond with your choice's corresponding letter.

                   a) Barbarian
                   b) Tank
                   c) Healer
                   d) Warrior
                Choose wisely, as your choice determines your strength, and the weapons that you will be using.\n\n""").lower()

while True:
    try:
        player = Player({"a": "barbarian", "b": "tank", "c": "healer", "d": "warrior"}.get(playertype))
        break
    except TypeError:
        playertype = input("\nHe tells you to just use the letter alone. Don't include brackets or anything.\n\n")

scene = ""

print("""At any time in this playthrough, you can use the following commands.
      1) stats -- This prints out your character's current statistics (e.g. their attack_strength, defense, etc.)
      2) scene -- This prints out the current scene using coloured ASCII art.
      3) help -- This will print out this exact string of text you are seeing right now!""")

stdinput = input

special_commands = {
    "stats": player.stats,
    "scene": scene,
    "help": """At any time in this playthrough, you can use the following commands.
    1) stats -- This prints out your character's current statistics (e.g. their attack_strength, defense, etc.)
    2) scene -- This prints out the current scene using coloured ASCII art.
    3) help -- This will print out this exact string of text you are seeing right now!"""}

def custom_input(prompt=""):
    
    while True:
        user_input = stdinput(prompt).strip().lower()
        if user_input in special_commands.keys():
            print(special_commands[user_input])
            continue
        return user_input

input = custom_input

def stdmvmt():
    mvmtdecision = input("""How would you like to move?

                         a) Up.
                         b) Down.
                         c) Left.
                         d) Right.""")
    while True:
        try:
            mvmtdecision = {"a": "up", "b": "down", "c": "left", "d": "right"}.get(mvmtdecision)
            break
        except TypeError:
            mvmtdecision = input("\nJust use the letter alone. Don't include brackets or anything.\n\n")

room1 = DungeonRoom(randint(15, 25), 1, player)
