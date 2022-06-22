from utils import *
from vec import Vec
from config import config
from window import controller

from entity.model.base import Model
from entity.view.base import View

class Entity:
    def __init__(self, level, pos):
        self.id = level.get_next_entity_id()
        self.alive = True

        self.touching_platform = False
        self.falling = False ## TODO - this is currently unused
        self.jumping = 0

        self.model = Model()
        self.view = View()

        self.pos = pos
        self.vel = Vec(0, 0)
        self.ground_normal = Vec(0, 0)

        # HUD data
        self.hp = 10
        self.max_hp = 10
        self.power = 0
        self.max_power = 240

    def get_uuid(self):
        return "entity" + str(self.id)

    def get_held_pos(self):
        return self.view.held_pos

    def get_hitbox(self):
        height_body = self.model.height_body - (self.model.sneak_height_diff if self.view.states["sneaking"] else 0)

        top_left = self.pos + Vec(self.model.x_offset, self.model.height_head)
        bottom_left = self.pos + Vec(self.model.x_offset, -height_body)
        top_right = top_left + Vec(self.model.width, 0)
        bottom_right = bottom_left + Vec(self.model.width, 0)

        return [
            top_left,
            top_right,
            bottom_right,
            bottom_left,
        ]

    def update(self):
        self.pos += self.vel

        # print(self.ground_normal @ Vec(0, 1))
        if self.touching_platform and self.ground_normal @ Vec(0, 1) > 0.64:
            self.jumping = 0 ## TODO - more checks are probably required here...

        ## TODO add animation logic here
        ## like "self.view.update()"

        return self.alive

    def jump(self, force):
        if self.touching_platform and self.jumping == 0 and not self.view.states["sneaking"]:
            self.jumping = 1
            self.vel += force

    def sneak(self):
        if not self.view.states["sneaking"]:
            # self.model.height_body -= self.model.sneak_height_diff
            self.view.states["sneaking"] = True

    def unsneak(self):
        # self.model.height_body += self.model.sneak_height_diff
        self.pos.y += self.model.sneak_height_diff
        self.view.states["sneaking"] = False


    def render(self, camera_pos):

        ## Render hitbox
        if config["debug"]:
            win = controller.win

            (
                top_left,
                top_right,
                bottom_right,
                bottom_left
            ) = self.get_hitbox()

            pygame.draw.rect(win, (0, 0, 0),
                (*((top_left - camera_pos).screen_coords()),
                (top_right - top_left).x, (top_left - bottom_left).y))

        self.view.render(self.pos, camera_pos)

    def damage(self, dmg, src, knockback=Vec(0,0)):
        """
        0: fall damage - 1: melee damage
        """
        controller.sound_ctrl.play_sound(controller.sounds["hurt"])
        self.hp -= dmg
        self.vel += knockback

    def kill(self):
        self.alive = False

    def check_inside(self, pos):
        """
        Return (True, penetration_vector) if pos is inside entity's hitbox, else (False, None)
        """
        if self.x < pos.x and self.x + (self.width) > pos.x and self.y + (self.heightHead) > pos.y and self.y - (self.heightBody) < pos.y:
            return (True, Vec((self.x + (self.width/2)) - pos.x, self.y - pos.y))
        else:
            return (False, None)
