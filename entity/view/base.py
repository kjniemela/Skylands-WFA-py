from utils import *
from vec import Vec
from window import controller

class View:
    def __init__(self):
        self.facing = 1
        self.aim = 0
        
        self.states = {
            "sneaking": False,
            "moving": False,
            "jumping": False,
        }

    def render(self, pos, camera_pos):

        win = controller.win
        entity_textures = controller.player_textures ## TODO - THIS SHOULD FETCH THE CORRECT ENTITY TEXTURES!
        ## TODO - refactor code so that these are not needed
        mouse_x, mouse_y = controller.mouse_pos
        facing = self.facing
        x, y = pos
        camera_x, camera_y = camera_pos

        self.aim = -math.degrees(math.atan2(mouse_y-(180+24), mouse_x-(240+16)))
        head_rot = self.aim
        head_rot_left = ((360+(head_rot))%360)-180
        
        if abs(head_rot)> 90:
            self.facing = -1
        else:
            self.facing = 1

        if facing == -1:
            blitRotateCenter(win, entity_textures["head"][-1], min(max(head_rot_left, -45), 45), (x,-y-(20)), (camera_x,camera_y))
        elif facing == 1:
            blitRotateCenter(win, entity_textures["head"][1], min(max(head_rot, -45), 45), (x,-y-(20)), (camera_x,camera_y))
