from entities import *

def lab(level):
    if not "doors" in level.__dir__():
        level.doors = {
            "door_1": [0, -21, -1, 120, 5],
            }
    if not "dclv" in level.data:
        level.data["dclv"] = 0
    for doorID in level.doors:
        door = level.controls[doorID]
        #print(distance(level.player.x, level.player.y, door.x, door.y))
        if distance(level.player.x+(level.player.width/2), level.player.y, door.x, level.doors[doorID][1]) < 75 and level.doors[doorID][0] < level.doors[doorID][3]:
            level.doors[doorID][0] += level.doors[doorID][4]
            door.y = level.doors[doorID][1] + (level.doors[doorID][0]*level.doors[doorID][2])
        elif level.doors[doorID][0] > 0:
            level.doors[doorID][0] -= level.doors[doorID][4]
            door.y = level.doors[doorID][1] + (level.doors[doorID][0]*level.doors[doorID][2])
    if level.controls["controller1"].is_dead:
        door = level.controls["door_c1"]
        if door.y > 340:
            level.data["dclv"] += 1
            door.y -= level.data["dclv"]
        else:
            door.y = 340
            level.data["dclv"] *= -0.5
            if level.data["dclv"] < -1:
                door.y -= level.data["dclv"]
            

scripts = {
    "lab": lab,
    }

def get_script(script):
    return scripts[script]
