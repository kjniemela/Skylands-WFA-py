from utils import *
from vec import Vec
from window import controller

## Default head texture in case entity is loaded directly
entity_textures = {
    "head": controller.load_entity_texture("player", "head.png"),
}

class View:
    def __init__(self):
        self.textures = entity_textures

        self.facing = 1
        self.aim = 0
        
        self.states = {
            "sneaking": False,
            "moving": False,
            "jumping": False,
        }

    def render(self, pos, camera_pos):

        win = controller.win
        ## TODO - refactor code so that these are not needed
        facing = self.facing
        x, y = pos
        camera_x, camera_y = camera_pos

        head_rot = self.aim
        head_rot_left = ((360+(head_rot))%360)-180
        
        if abs(head_rot)> 90:
            self.facing = -1
        else:
            self.facing = 1

        if facing == -1:
            blitRotateCenter(win, self.textures["head"][-1], min(max(head_rot_left, -45), 45), (x,-y-(20)), (camera_x,camera_y))
        elif facing == 1:
            blitRotateCenter(win, self.textures["head"][1], min(max(head_rot, -45), 45), (x,-y-(20)), (camera_x,camera_y))
