from playerclass import Player, Enemy
from roomdefinitions import DungeonRoom

playertype = input("""You will soon embark on your journey, fighting the horrible Glitch.
            A kind wizard appears next to you. He asks what class you would like to play.
        He gives you the following four options, and tells you to respond with your choice's corresponding letter.

                   a) Barbarian
                   b) Tank
                   c) Healer
                   d) Warrior
                Choose wisely, as your choice determines your strength, and the weapons that you will be using.\n\n""")

player = Player({"a": "barbarian", "b": "tank", "c": "healer", "d": "warrior"}.get(playertype))

