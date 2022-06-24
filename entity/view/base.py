from utils import *
from vec import Vec
from window import controller

from entity.view.component import Component

## Default head texture in case entity is loaded directly
entity_textures = {
    "head": controller.load_entity_texture("player", "head.png"),
}

class View:
    def __init__(self, is_super=False):
        self.textures = entity_textures

        self.facing = 1
        self.aim = 0
        
        self.states = {
            "sneaking": False,
            "moving": False,
            "jumping": False,
        }

        if not is_super: ## small, probably unnecessary optimization
            self.def_components()

    def def_components(self):
        self.components = {
            "head": Component(self.textures["head"], Vec(19, 2), Vec(21, 2), Vec(0, -9)),
        }

    def render_component(self, component_name, angle, pos, camera_pos):
        component = self.components[component_name]
        component.set_angle(angle)
        blitRotateAround(
            controller.win,
            component.texture[self.facing],
            component.get_angle() * self.facing,
            pos + component.get_offset(self.facing),
            camera_pos,
            component.pivot
        )

    def render(self, pos, camera_pos):

        head_rot = self.aim
        
        if abs(head_rot)> 90:
            self.facing = -1
        else:
            self.facing = 1

        if self.facing == -1: head_rot = -(((360+(head_rot))%360)-180)

        self.render_component("head", min(max(head_rot, -45), 45), pos, camera_pos)
