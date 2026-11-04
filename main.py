import random
import os, sys

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

#set starting stats.
health = 3
power = 3
treasure = 0
clues = 0
kills = 0
# changeing any stat except health is always +1 (while health also has -1 as possibility)
def change_stat(stat):
    global health
    global power
    global treasure
    global clues
    global kills
    match stat:
        case "power":
            print("increase power")
            power = power +1
        case "treasure":
            print("found a treasure! YAY!")
            treasure = treasure +1
        case "+":
            print("potion found")
            health = health +1
        case "-":
            print("ouch, that hurt")
            health = health -1
        case "clue":
            print("found a clue about the boss here")
            clues = clues +1
            if clues%2 == 0:
                power = power +1
        case "kill":
            print("take that villain!")
            kills = kills +1
            if kills%3 == 0:
                power = power +1
    return

#room functions
def nothing():
    print("empty room")
    return
def trap():
    print("trap encounter")
    result = random.randint(1,6)
    if result == 6:
        print("diffused, and would you look at that!")
        change_stat("treasure")
    if result == 5:
        print("diffused, and would you look at that!")
        change_stat("clue")
    if result == 3 or result == 4:
        "dodged it, phew"
    if result == 2 or result == 1:
        change_stat("-")
    return "trap"

def fight_crit_RAW(hp, strenght):
    while hp > 0:
        e_roll = random.randint(1,6)
        p_roll = random.randint(1,6)
        e_hit = e_roll + strenght
        p_hit = p_roll + power
        if e_hit > p_hit:
            change_stat("-")
            if e_roll == 6:
                change_stat("-")
            if p_roll == 6:
                hp = hp-2
        elif e_hit < p_hit:
            print("hit em good")
            hp = hp -1
            if p_roll == 6:
                print("real good")
                hp = hp -1
            if e_roll == 6:
                change_stat("-")
                change_stat("-")
    return
def fight(hp, strenght):
    while hp > 0:
        e_roll = random.randint(1,6)
        p_roll = random.randint(1,6)
        e_hit = e_roll + strenght
        p_hit = p_roll + power
        if e_hit > p_hit:
            change_stat("-")
            if e_roll == 6:
                change_stat("-")
        elif e_hit < p_hit:
            print("hit em good")
            hp = hp -1
            if p_roll == 6:
                print("real good")
                hp = hp -1
    return

#choosing the monster and cue fight
def monster():
    skeleton = [2,2, "skeleton"]
    ghost = [1, 2, "ghost"]
    ooze = [3, 1, "ooze"]
    mimic = [3, 2, "mimic"]
    beast = [4, 2, "beast"]
    goblin = [2, 1, "goblin"]
    creatures = [skeleton, ghost, ooze, mimic, beast, goblin]
    enemy = random.choice(creatures)
    print("fight a " + enemy[2] + "!")
    fight(enemy[0], enemy[1])
    if health <= 0:
        return enemy[2]
    change_stat("kill")

#choosing the boss and cue fight
def boss():
    humanoid = [4, 4, "humanoid"]
    beast = [5, 5, "beast"]
    undead = [5, 4, "undead"]
    monstrosity = [6, 4, "monstrosity"]
    construct = [6, 5, "construct"]
    aberration = [6, 6, "aberration"]
    creatures = [humanoid, beast, undead, monstrosity, construct, aberration]
    enemy = random.choice(creatures)
    print("fight a " + enemy[2] + "!")
    fight(enemy[0], enemy[1])
    return "boss"

#roll a room, with 3 of the options resulting in only a stat change
def roll_content():
    result = random.randint(1, 6)
    death = "uhm not yet"
    match result:
        case 6:
            change_stat("clue")
        case 5:
            change_stat("+")
        case 4:
            change_stat("treasure")
        case 3:
            death = monster()
        case 2:
            death = trap()
        case 1:
            nothing()

    return death

def game_loop(rooms):
    while health > 0:
        # if you wish to see the course of a run, remove the "with hiddenpringt():"
        with HiddenPrints():
            death = roll_content()
        rooms = rooms - 1
        if rooms == 1:
            # if you wish to see the course of a run, remove the "with hiddenpringt():"
            with HiddenPrints():
                boss()
            if health > 0:
                # if you wish to see the course of a run, remove the "#"
    #            print("Boss killed")
                match treasure:
                    case 0:
                        print("Survivor")
                    case 1:
                        print("Adventurer")
                    case 2:
                        print("Adventurer")
                    case 3:
                        print("Explorer")
                    case 4:
                        print("Explorer")
                    case 5:
                        print("Explorer")
                    case 6:
                        print("Hero")
                    case 7:
                        print("Hero")
                    case 8:
                        print("Hero")
                    case _:
                        print("Legend")

                print("treasure found: " + str(treasure))
                print("clues found: " + str(clues))
                print("kills: " + str(kills))
                print("total power: " + str(power))
                print("remaining health: " + str(health))
                return [treasure, clues, kills, power, health]

    print("you died to a " + str(death))
    return rooms

if __name__ == '__main__':
    runs = 10000 # the number of runs to simulate
    deaths = 0
    stats = [0, 0, 0, 0, 0]
    rooms_left = 0
    # if you wish to see the stats of a run, remove the "with hiddenpringt():"
    with HiddenPrints():
        for i in range(0,runs):
            result = game_loop(35)
            if type(result) is int:
                deaths = deaths +1
                rooms_left = rooms_left + result
            else:
                stats = [x + y for x, y in zip(stats, result)]
            health = 3
            power = 3
            treasure = 0
            clues = 0
            kills = 0

    print("died " + str(deaths) + " times ("+ str(round(deaths/runs*100,2)) + "%) with an average of " + str(round(rooms_left/deaths,2)) + " rooms left")
    print("succeeded " + str(runs-deaths) + " times ("+ str(round((runs-deaths)/runs*100,2)) + "%) with average stats as follows:")
    stats_average = [round(x / (runs-deaths),2) for x in stats]
    print("treasure found: " + str(stats_average[0]))
    print("clues found: " + str(stats_average[1]))
    print("kills: " + str(stats_average[2]))
    print("total power: " + str(stats_average[3]))
    print("remaining health: " + str(stats_average[4]))