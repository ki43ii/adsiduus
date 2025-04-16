from playerclass import *
from roomdefinitions import *
from random import *
from sprites import *
from ast import literal_eval
from sys import exit

savedec = input("""Before you begin, a wizard appears to you and says something strange about savefiles. Though your character is confused as to what he is talking about, perhaps you might understand.

        He asks which savefile you would like to load.

            1) Save 1
            2) Save 2
            3) Save 3
            4) Save 4
            5) List the stats of each save.\n\n\n\n""")

while True:

    if savedec == "5":

        for i in range(1,5):

            with open(f"savefiles/savefile-{i}.txt", "r") as savefile:
                values = savefile.read()
            
            print(f"""Savefile {i}:

                  {values}""")

        savedec = input("\n\nNow, you can make your decision. Which savefile would you like to load?\n\n\n\n")
    
    elif savedec not in ("1", "2", "3", "4"):
        savedec = input(f"You try to load save {savedec}, but it doesn't exist. Choose something else.\n\n\n\n")

    else:
        break
    
savefile = f"savefiles/savefile-{savedec}.txt"

with open(savefile, "r") as save:
    save = save.read()
    save = literal_eval(save)

if save.get("playertype") == "TBD":

    playertype = input("""You will soon embark on your journey, fighting the horrible Glitch.
            A kind wizard appears next to you. He asks what class you would like to play.
        He gives you the following four options, and tells you to respond with your choice's corresponding letter.

                   a) Barbarian
                   b) Tank
                   c) Healer
                   d) Warrior
                Choose wisely, as your choice determines your strength, and the weapons that you will be using.\n\n""").lower()

    while True:
        if playertype in ("a", "b", "c", "d"):
            player = Player({"a": "barbarian", "b": "tank", "c": "healer", "d": "warrior"}.get(playertype), save, savefile)
            break
        else:
            playertype = input("\nHe tells you to just use the letter alone. Don't include brackets or anything.\n\n")

else:
    player = Player(save.get("playertype"), save, savefile)

scene = ""

print("""At any time in this playthrough, you can use the following commands:-

      1) stats -- This prints out your character's current statistics (e.g. their attack_strength, defense, etc.)
      2) scene -- This prints out the current scene using coloured ASCII art.
      3) help -- This will print out this exact string of text you are seeing right now!
      4) credits -- This will tell you the collaborators on this game, and what they've contributed.
      5) exit/quit -- These will quit out of the game. Don't worry, your progress will be saved to the savefile you chose.
      6) save -- This will manually save your progress (including what room you're in, your health, your level, etc.). Don't worry though, the game will auto-save every time you take damage, go to a new room, etc..\n""")

import builtins as b  # looks wonky but i need to do this

stdinput = input

special_commands_func = {
    "exit": lambda: exit(),
    "quit": lambda: exit(),
    "save": lambda: player.save()}

special_commands = {
    "stats": player.stats,
    "scene": scene,
    "help": """At any time in this playthrough, you can use the following commands.
    1) stats -- This prints out your character's current statistics (e.g. their attack_strength, defense, etc.)
    2) scene -- This prints out the current scene using coloured ASCII art.
    3) help -- This will print out this exact string of text you are seeing right now!
    4) credits -- This will tell you the collaborators on this game, and what they've contributed.
    5) exit/quit -- These will quit out of the game. Don't worry, your progress will be saved to whatever savefile you chose.
    6) save -- This will manually save your progress (including what room you're in, your health, your level, etc.). Don't worry though, the game will auto-save every time you take damage, go to a new room, etc..\n""",
    "credits": """
    All the code        --          Fredrick Wans   8U
    95% of sprites      --          Hassan Saheb    8K
    5% of sprites       --          Ahmed Sayed     8E
    Emotional support   --          Mohamed Khalil  8A\n\n"""}
    

def custom_input(prompt=""):
    
    while True:
        user_input = stdinput(prompt).strip().lower()
        if user_input in special_commands.keys():
            print(special_commands[user_input])
            continue
        elif user_input in special_commands_func.keys():
            special_commands_func[user_input]()
            continue
        return user_input

b.input = custom_input

def stdmvmt():
    mvmtdecision = input("""\n\nYou can now move in any direction. You can also see a map of the rooms you've been to and what is around you.

                         a) Up.
                         b) Down.
                         c) Left.
                         d) Right.
                         e) Map.\n\n""")


    while True:
        if mvmtdecision in ("a", "b", "c", "d", "e"):
            break
        else:
            mvmtdecision = input("\nJust use the letter alone. Don't include brackets or anything.\n\n\n")
    return mvmtdecision

maparr = []

for _ in range(11):
    maparr.append([0,0,0,0,0,0,0,0,0,0,0])

cur_room = save.get("checkpoint")

if cur_room != None:
    print(f"\nYou left off last time in a {save.get('checkpoint')} room.")
else:
    print("\n\nYou wake up in a completely empty room; all by yourself. Four doors appear at your front, back, left and right. You realise that you'll be stuck here quite a while...")
    cur_room = "start"
    player.save()

difficulty = (player.level // 3.5) + 1

rooms = (lambda: ShootRoom(difficulty, player),
         lambda: DungeonRoom(randint(15,25), difficulty, player),
         lambda: DungeonRoom(randint(15,25), difficulty, player),
         lambda: TripleDoorRoom(difficulty, player),
         lambda: TripleDoorRoom(difficulty, player),
         lambda: TripleDoorRoom(difficulty, player),
         lambda: EmptyRoom(player),
         lambda: EmptyRoom(player),
         lambda: EmptyRoom(player))
formatted_rooms = ("Shoot Room", "Dungeon Room", "Dungeon Room", "Three Doors", "Three Doors", "Three Doors", "Empty Room", "Empty Room", "Empty Room")

if cur_room == "dungeon":
    room = DungeonRoom(randint(15,25), difficulty, player)
elif cur_room == "triple door":
    room = TripleDoorRoom(difficulty, player)
elif cur_room == "shoot":
    room = ShootRoom(difficulty, player)
elif cur_room == "empty":
    room = EmptyRoom(player)

def render_minimap(gamemap, maparr, pos):
    ROOM_WIDTH = 33
    ROOM_HEIGHT = 22
    GRID_SIZE = len(maparr)

    # Create a blank canvas the same size as gamemap (or copy it)
    minimap_canvas = "\n".join([" " * 99 for _ in range(66)])

    py, px = pos  # player y and x

    for dy in range(-1, 2):  # -1, 0, 1
        for dx in range(-1, 2):
            ny, nx = py + dy, px + dx

            if 0 <= ny < GRID_SIZE and 0 <= nx < GRID_SIZE:
                cell = maparr[ny][nx]

                if cell == 0:
                    label = "???"
                elif ny == py and nx == px:
                    label = "[YOU]"
                else:
                    label = cell

                # Center label in room block
                room_art = generate_room_block(label)

                # Calculate top-left corner for this cell in the ascii canvas
                canvas_x = (dx + 1) * ROOM_WIDTH  # shift -1..1 → 0..2
                canvas_y = (dy + 1) * ROOM_HEIGHT

                minimap_canvas = overlayer(minimap_canvas, room_art, box=(canvas_x, canvas_y))

    return minimap_canvas

while True:

    mvmt_dir = stdmvmt()
    if mvmt_dir == "a":
	    pos[0] -= 1
    elif mvmt_dir == "b":
	    pos[0] += 1
    elif mvmt_dir == "c":
	    pos[1] -= 1
    elif mvmt_dir == "d":
        pos[1] += 1
    else:
        print(render_minimap())

    roomchoice = randint(0,8)
    
    maparr[pos[0]][pos[1]] = formatted_rooms[roomchoice]
    room = rooms[roomchoice]()
