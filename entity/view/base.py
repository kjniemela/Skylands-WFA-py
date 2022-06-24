from utils import *
from vec import Vec
from window import controller

from entity.view.component import Component

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

        self.components = {
            "head": Component(entity_textures["head"], Vec(20, 0), Vec(20, 0), Vec(0, -10)),
        }

        self.head_offset = Vec(0, 20)

    def render_component(self, component_name, angle, pos, camera_pos):
        component = self.components[component_name]
        blitRotateAround(
            controller.win,
            component.texture[self.facing],
            angle,
            pos + component.offset[self.facing],
            camera_pos,
            component.pivot
        )

    def render(self, pos, camera_pos):

        head_rot = self.aim
        
        if abs(head_rot)> 90:
            self.facing = -1
        else:
            self.facing = 1

        if self.facing == -1: head_rot = ((360+(head_rot))%360)-180

        self.render_component("head", min(max(head_rot, -45), 45), pos, camera_pos)
