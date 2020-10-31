from entities import *

def lab(level):
    if not "doors" in level.__dir__():
        level.doors = {
            "door_1": [0, -21, -1, 120, 5],
            }
    for doorID in level.doors:
        door = level.controls[doorID]
        #print(distance(level.player.x, level.player.y, door.x, door.y))
        if distance(level.player.x+(level.player.width/2), level.player.y, door.x, level.doors[doorID][1]) < 75 and level.doors[doorID][0] < level.doors[doorID][3]:
            level.doors[doorID][0] += level.doors[doorID][4]
            door.y = level.doors[doorID][1] + (level.doors[doorID][0]*level.doors[doorID][2])
        elif level.doors[doorID][0] > 0:
            level.doors[doorID][0] -= level.doors[doorID][4]
            door.y = level.doors[doorID][1] + (level.doors[doorID][0]*level.doors[doorID][2])

scripts = {
    "lab": lab,
    }

def get_script(script):
    return scripts[script]
