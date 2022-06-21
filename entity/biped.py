from utils import *
from vec import Vec
from config import config
from window import controller

from entity.base import Entity
from entity.model.base import Model
from entity.view.biped import ViewBiped

class EntityBiped(Entity):
    def __init__(self, level, pos):
        super().__init__(level, pos)

        self.model = Model()
        self.view = ViewBiped()

        self.gun_cooldown = 0
        self.reload_speed = 2
        self.reload = True

        self.pos = pos
        self.vel = Vec(0, 0)

    # def update(self):
    #     return super().update()

    def render(self, camera_pos):

        ## TODO more logic to decide if sounds should be played... or maybe volume/pan control?
        if (self.view.walk_frame == 10 or self.view.walk_frame == 25) and self.touching_platform:
            controller.sound_ctrl.play_sound(controller.sounds["step%i"%(randint(1, 3))])

        super().render(camera_pos)
