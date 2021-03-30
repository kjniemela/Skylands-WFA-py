from entities import *

def lab(level):
    if not "doors" in level.__dir__():
        level.doors = {
            "door_1": [0, -21, -1, 120, 5, False, False],
            }
    if not "dclv" in level.data:
        level.data["dclv"] = 0
    for doorID in level.doors:
        door = level.controls[doorID]
        #print(distance(level.player.x, level.player.y, door.x, door.y))
        if distance(level.player.x+(level.player.width/2), level.player.y, door.x, level.doors[doorID][1]) < 75 and level.doors[doorID][0] < level.doors[doorID][3]:
            level.doors[doorID][0] += level.doors[doorID][4]
            door.y = level.doors[doorID][1] + (level.doors[doorID][0]*level.doors[doorID][2])
            if not level.doors[doorID][5]:
                level.doors[doorID][6] = False
                level.doors[doorID][5] = True
                level.play_sound('door_open')
        elif level.doors[doorID][0] > 0:
            level.doors[doorID][0] -= level.doors[doorID][4]
            door.y = level.doors[doorID][1] + (level.doors[doorID][0]*level.doors[doorID][2])
            if not level.doors[doorID][6] and level.doors[doorID][0] < (level.doors[doorID][3]*0.9):
                level.doors[doorID][6] = True
                level.play_sound('door_close')
            if level.doors[doorID][0] < (level.doors[doorID][3]//2):
                level.doors[doorID][5] = False
    if level.controls["controller1"].is_dead:
        door = level.controls["door_c1"]
        if door.y > 340:
            if level.data["dclv"] == 0:
                level.play_sound('door_open')
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
