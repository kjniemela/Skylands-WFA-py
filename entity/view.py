from utils import *
from vec import Vec
from window import controller

class View:
    def __init__(self):
        self.walk_frame = 0
        self.facing = 1
        
        self.states = {
            "sneaking": False,
            "moving": False,
            "jumping": False,
        }

        # rotation of entity's arms
        self.right_arm = 0
        self.left_arm = 0
        self.right_hand = 0
        self.left_hand = 0

        # position of item held by entity
        self.held_pos = Vec(0, 0)

    def render(self, pos, camera_pos):

        win = controller.win
        entity_textures = controller.player_textures ## TODO - THIS SHOULD FETCH THE CORRECT ENTITY TEXTURES!
        ## TODO - refactor code so that these are not needed
        mouse_x, mouse_y = controller.mouse_pos
        facing = self.facing
        x, y = pos
        camera_x, camera_y = camera_pos

        head_rot = -math.degrees(math.atan2(mouse_y-(180+24), mouse_x-(240+16)))
        head_rot_left = ((360+(head_rot))%360)-180
        self.aim = head_rot
        
        if abs(head_rot)> 90:
            self.facing = -1
        else:
            self.facing = 1
        
        if self.walk_frame + 1 >= 32:
            self.walk_frame = 0
        if self.walk_frame < 0:
            self.walk_frame = 30

        head_rot_left = ((360+(head_rot))%360)-180
        self.right_arm = head_rot-(15*facing)#(Sin((time()+1)*40)*10)-90-(5*self.facing)#
        self.left_arm = (Sin(time()*40)*10)-90-(5*facing)
        self.right_hand = 15
        self.left_hand = 10

        # arm position is a bit buggy
        
        if facing == -1:
            blitRotateCenter(win, entity_textures["arm_far"][-1], self.right_arm, (x-(3),-y-(2)), (camera_x,camera_y))
            hand_x = (x-(8))+(Cos(-self.right_arm)*(11))
            hand_y = (-y-(0))+(Sin(-self.right_arm)*(11))
            self.held_x = (hand_x+(8))+(Cos(-(self.right_arm-self.right_hand))*(15))
            self.held_y = hand_y+(Sin(-(self.right_arm-self.right_hand))*(16))
            blitRotateCenter(win, entity_textures["hand_far"][-1], self.right_arm-self.right_hand, (hand_x,hand_y), (camera_x,camera_y))
            blitRotateCenter(win, controller.items["GDFSER"][-1], self.right_arm-self.right_hand, (self.held_x,self.held_y), (camera_x,camera_y))
        elif facing == 1:
            blitRotateCenter(win, entity_textures["arm_far"][1], self.left_arm, (x+(15),-y-(2)), (camera_x,camera_y))
            hand_x = (x+(11))+(Cos(-self.left_arm)*(11))
            hand_y = (-y-(0))+(Sin(-self.left_arm)*(11))
            blitRotateCenter(win, entity_textures["hand_far"][1], self.left_arm+self.left_hand, (hand_x,hand_y), (camera_x,camera_y))

        if self.states["sneaking"]:
            win.blit(entity_textures["sneak"][facing], (x-camera_x+3,-(y-camera_y)) if self.facing < 0 else (x-camera_x-7,-(y-camera_y)))
        else:
            if self.states["moving"]:
                win.blit(entity_textures["walk"][facing][self.view.walk_frame//4], (x-camera_x,-(y-camera_y)))
            else:
                win.blit(entity_textures["idle"][facing], (x-camera_x,-(y-camera_y)))

        if facing == -1:
            blitRotateCenter(win, entity_textures["head"][-1], min(max(head_rot_left, -45), 45), (x,-y-(20)), (camera_x,camera_y))
        elif facing == 1:
            blitRotateCenter(win, entity_textures["head"][1], min(max(head_rot, -45), 45), (x,-y-(20)), (camera_x,camera_y))

        if facing == -1:
            blitRotateCenter(win, entity_textures["arm_near"][-1], -self.left_arm, (x+17,-y-0), (camera_x,camera_y))
            hand_x = (x+(12))-(Cos(-self.left_arm)*(11))
            hand_y = (-y-(0))+(Sin(-self.left_arm)*(11))
            blitRotateCenter(win, entity_textures["hand_near"][-1], -self.left_arm-self.left_hand, (hand_x,hand_y), (camera_x,camera_y))
        elif facing == 1:
            blitRotateCenter(win, entity_textures["arm_near"][1], self.right_arm, (x-2,-y-(2)), (camera_x,camera_y))
            hand_x = (x-(8))+(Cos(-self.right_arm)*(11))
            hand_y = (-y-(0))+(Sin(-self.right_arm)*(11))
            self.held_x = (hand_x+(8))+(Cos(-(self.right_arm+self.right_hand))*(15))
            self.held_y = hand_y+(Sin(-(self.right_arm+self.right_hand))*(16))
            blitRotateCenter(win, controller.items["GDFSER"][1], self.right_arm+self.right_hand, (self.held_x,self.held_y), (camera_x,camera_y))
            blitRotateCenter(win, entity_textures["hand_near"][1], self.right_arm+self.right_hand, (hand_x,hand_y), (camera_x,camera_y))
