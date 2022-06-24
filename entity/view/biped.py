from utils import *
from vec import Vec
from window import controller

from entity.view.base import View

## Default textures in case entityBiped is loaded directly
entity_biped_textures = {
    "torso": controller.load_entity_texture("player", "torso.png"),
    "arm_near": controller.load_entity_texture("player", "arm_near.png"),
    "arm_far": controller.load_entity_texture("player", "arm_far.png"),
    "hand_near": controller.load_entity_texture("player", "hand_near.png"),
    "hand_far": controller.load_entity_texture("player", "hand_far.png"),
    "leg_near": controller.load_entity_texture("shoaldier", "leg_near.png"),
    "leg_far": controller.load_entity_texture("shoaldier", "leg_far.png"),
    "foot_near": controller.load_entity_texture("shoaldier", "foot_near.png"),
    "foot_far": controller.load_entity_texture("shoaldier", "foot_far.png"),
}

class ViewBiped(View):
    def __init__(self):
        super().__init__()

        self.textures = {
            **self.textures,
            **entity_biped_textures,
        }

        self.walk_frame = 0

        # rotation of entity's arms
        self.right_arm = 0
        self.left_arm = 0
        self.right_hand = 0
        self.left_hand = 0

        # position of item held by entity
        self.held_pos = Vec(0, 0)

    def render(self, pos, camera_pos):

        win = controller.win
        # self.textures = controller.player_textures ## TODO - THIS SHOULD FETCH THE CORRECT ENTITY TEXTURES!
        ## TODO - refactor code so that these are not needed
        facing = self.facing
        x, y = pos
        camera_x, camera_y = camera_pos
        
        if self.walk_frame + 1 >= 32:
            self.walk_frame = 0
        if self.walk_frame < 0:
            self.walk_frame = 30

        self.right_arm = self.aim-(15*facing)#(Sin((time()+1)*40)*10)-90-(5*self.facing)#
        self.left_arm = (Sin(time()*40)*10)-90-(5*facing)
        self.right_hand = 15
        self.left_hand = 10

        # arm position is a bit buggy
        
        # if facing == -1:
        #     blitRotateCenter(win, self.textures["arm_far"][-1], self.right_arm, (x-(3),-y-(2)), (camera_x,camera_y))
        #     hand_x = (x-(8))+(Cos(-self.right_arm)*(11))
        #     hand_y = (-y-(0))+(Sin(-self.right_arm)*(11))
        #     self.held_pos.x = (hand_x+(8))+(Cos(-(self.right_arm-self.right_hand))*(15))
        #     self.held_pos.y = hand_y+(Sin(-(self.right_arm-self.right_hand))*(16))
        #     blitRotateCenter(win, self.textures["hand_far"][-1], self.right_arm-self.right_hand, (hand_x,hand_y), (camera_x,camera_y))
        #     blitRotateCenter(win, controller.items["GDFSER"][-1], self.right_arm-self.right_hand, (self.held_pos.x,self.held_pos.y), (camera_x,camera_y))
        # elif facing == 1:
        #     blitRotateCenter(win, self.textures["arm_far"][1], self.left_arm, (x+(15),-y-(2)), (camera_x,camera_y))
        #     hand_x = (x+(11))+(Cos(-self.left_arm)*(11))
        #     hand_y = (-y-(0))+(Sin(-self.left_arm)*(11))
        #     blitRotateCenter(win, self.textures["hand_far"][1], self.left_arm+self.left_hand, (hand_x,hand_y), (camera_x,camera_y))

        # if facing == -1:
        #     blitRotateCenter(win, self.textures["leg_far"][-1], self.right_arm, (x-(3),-y-(2)), (camera_x,camera_y))
        #     hand_x = (x-(8))+(Cos(-self.right_arm)*(11))
        #     hand_y = (-y-(0))+(Sin(-self.right_arm)*(11))
        #     self.held_pos.x = (hand_x+(8))+(Cos(-(self.right_arm-self.right_hand))*(15))
        #     self.held_pos.y = hand_y+(Sin(-(self.right_arm-self.right_hand))*(16))
        #     # blitRotateCenter(win, self.textures["hand_far"][-1], self.right_arm-self.right_hand, (hand_x,hand_y), (camera_x,camera_y))
        #     # blitRotateCenter(win, controller.items["GDFSER"][-1], self.right_arm-self.right_hand, (self.held_pos.x,self.held_pos.y), (camera_x,camera_y))
        # elif facing == 1:
        #     blitRotateCenter(win, self.textures["leg_far"][1], self.left_arm, (x+(15),-y-(2)), (camera_x,camera_y))
        #     hand_x = (x+(11))+(Cos(-self.left_arm)*(11))
        #     hand_y = (-y-(0))+(Sin(-self.left_arm)*(11))
        #     # blitRotateCenter(win, self.textures["hand_far"][1], self.left_arm+self.left_hand, (hand_x,hand_y), (camera_x,camera_y))

        # blitRotateCenter(win, self.textures['torso'][self.facing], 0, (x + 11, -y), (camera_x, camera_y))

        super().render(pos, camera_pos)

        # if facing == -1:
        #     blitRotateCenter(win, self.textures["arm_near"][-1], -self.left_arm, (x+17,-y-0), (camera_x,camera_y))
        #     hand_x = (x+(12))-(Cos(-self.left_arm)*(11))
        #     hand_y = (-y-(0))+(Sin(-self.left_arm)*(11))
        #     blitRotateCenter(win, self.textures["hand_near"][-1], -self.left_arm-self.left_hand, (hand_x,hand_y), (camera_x,camera_y))
        # elif facing == 1:
        #     blitRotateCenter(win, self.textures["arm_near"][1], self.right_arm, (x-2,-y-(2)), (camera_x,camera_y))
        #     hand_x = (x-(8))+(Cos(-self.right_arm)*(11))
        #     hand_y = (-y-(0))+(Sin(-self.right_arm)*(11))
        #     self.held_pos.x = (hand_x+(8))+(Cos(-(self.right_arm+self.right_hand))*(15))
        #     self.held_pos.y = hand_y+(Sin(-(self.right_arm+self.right_hand))*(16))
        #     blitRotateCenter(win, controller.items["GDFSER"][1], self.right_arm+self.right_hand, (self.held_pos.x,self.held_pos.y), (camera_x,camera_y))
        #     blitRotateCenter(win, self.textures["hand_near"][1], self.right_arm+self.right_hand, (hand_x,hand_y), (camera_x,camera_y))
