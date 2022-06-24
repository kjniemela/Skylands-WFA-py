from utils import *
from vec import Vec
from window import controller

from entity.view.base import View
from entity.view.component import Component

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
    def __init__(self, is_super=False):
        super().__init__(is_super=True)

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

        if not is_super: ## small, probably unnecessary optimization
            self.def_components()

    def def_components(self):
        super().def_components()

        self.components = {
            **self.components,
            "torso": Component(self.textures["torso"], Vec(20, -12), Vec(20, -12), Vec(0, 0)),
            "arm_near": Component(self.textures["arm_near"], Vec(30, -5), Vec(10, -5), Vec(0, 4)),
            "arm_far": Component(self.textures["arm_far"], Vec(10, -5), Vec(30, -5), Vec(0, 4)),
            "hand_near": Component(self.textures["hand_near"], Vec(0, -12), Vec(0, -12), Vec(0, 8)),
            "hand_far": Component(self.textures["hand_far"], Vec(1, -12), Vec(-1, -12), Vec(0, 8)),
        }

        self.components["hand_near"].set_parent(self.components["arm_near"])
        self.components["hand_far"].set_parent(self.components["arm_far"])

    def render(self, pos, camera_pos):
        
        if self.walk_frame + 1 >= 32:
            self.walk_frame = 0
        if self.walk_frame < 0:
            self.walk_frame = 30

        aim = self.aim if self.facing == 1 else -(((360+(self.aim))%360)-180)

        self.right_arm = aim-15+90#(Sin((time()+1)*40)*10)-90-(5*self.facing)#
        self.left_arm = (Sin(time()*40)*10)-5
        self.right_hand = 15
        self.left_hand = 10

        self.render_component("arm_far", self.left_arm if self.facing == 1 else self.right_arm, pos, camera_pos)
        if self.facing == -1:
            hand_angle = -self.components["hand_far"].get_angle()
            self.held_pos = pos + self.components["hand_far"].get_offset(-1) + Vec(0, -20).rotate(hand_angle)
            blitRotateAround(controller.win, controller.items["GDFSER"][-1], hand_angle - 90, self.held_pos, camera_pos, Vec(0, 0))
        self.render_component("hand_far", self.left_hand if self.facing == 1 else self.right_hand, pos, camera_pos)

        self.render_component("torso", 0, pos, camera_pos)

        super().render(pos, camera_pos)

        self.render_component("arm_near", self.right_arm if self.facing == 1 else self.left_arm, pos, camera_pos)
        if self.facing == 1:
            hand_angle = self.components["hand_near"].get_angle()
            self.held_pos = pos + self.components["hand_near"].get_offset(1) + Vec(0, -20).rotate(hand_angle)
            blitRotateAround(controller.win, controller.items["GDFSER"][1], hand_angle - 90, self.held_pos, camera_pos, Vec(0, 0))
        self.render_component("hand_near", self.right_hand if self.facing == 1 else self.left_hand, pos, camera_pos)