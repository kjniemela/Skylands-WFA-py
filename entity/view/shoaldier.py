from utils import *
from vec import Vec
from window import controller

from entity.view.biped import ViewBiped
from entity.view.component import Component

entity_shoaldier_textures = {
    "head": controller.load_entity_texture("shoaldier", "head.png"),
    "torso": controller.load_entity_texture("shoaldier", "torso.png"),
    "arm_near": controller.load_entity_texture("shoaldier", "arm_near.png"),
    "arm_far": controller.load_entity_texture("shoaldier", "arm_far.png"),
    "hand_near": controller.load_entity_texture("shoaldier", "hand_near.png"),
    "hand_far": controller.load_entity_texture("shoaldier", "hand_far.png"),
    "leg_near": controller.load_entity_texture("shoaldier", "leg_near.png"),
    "leg_far": controller.load_entity_texture("shoaldier", "leg_far.png"),
    "foot_near": controller.load_entity_texture("shoaldier", "foot_near.png"),
    "foot_far": controller.load_entity_texture("shoaldier", "foot_far.png"),
}

class ViewShoaldier(ViewBiped):
    def __init__(self, is_super=False):
        super().__init__(is_super=True)

        self.textures = {
            **entity_shoaldier_textures,
        }

        if not is_super: ## small, probably unnecessary optimization
            self.def_components()

    def def_components(self):
        super().def_components()

        # self.components = {
        #     **self.components,
        # }

    def render(self, pos, camera_pos):

        super().render(pos, camera_pos)