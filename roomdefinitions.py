from playerclass import Enemy, Player
from collections import Counter

# this will be useful in the allattack method
def format_enemyarray(arr):
    enemy_counts = Counter(arr)  # Count occurrences of each number
    sorted_enemy_counts = sorted(enemy_counts.items(), key=lambda item: item[1], reverse=True)  # Sort by count descending
    
    formatted_result = []
    for enemy, count in sorted_enemy_counts:
        if count == 1:
            formatted_result.append(f"a {enemy}")
        elif 
        else:
            formatted_result.append(f"{number_encoding.get(count)} {enemy}s")
    
    return formatted_result

number_encoding = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve",
                   13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty"}
player = Player("barbarian")

class DungeonRoom:

    def __init__(self, enemycount):
        
        self.contained_enemies = []
        for i in range(enemycount):
            self.contained_enemies.append(Enemy(10))

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

        hitenemies, missenemies = format_enemyarray(hitenemies), format_enemyarray(missenemies)

        if hitenemies:
            # converting hitenemies and missenemies to strings
            hitenemiesstr = hitenemies[0]
            for item in hitenemies[1:]: hitenemiesstr += f", {item}"
        
        missenemiesstr = missenemies[0]
        for item in missenemies: missenemiesstr += f", {item}"

        print(f"""Lucky you! You have managed to dodge {totaldamagemissed} hit points worth of damage from {missenemiesstr}.""")
        if totaldamagehit > 0:
            print(f"""However, you were unable to avoid {totaldamagehit} hit points worth of damage from {hitenemiesstr}.""")

dungeon = DungeonRoom(20)

dungeon.allattack_player(player)
