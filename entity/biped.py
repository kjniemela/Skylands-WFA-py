from utils import *
from vec import Vec
from config import config
from window import controller

from entity.base import Entity
from entity.model.base import Model
from entity.view.biped import ViewBiped
from projectile import Bullet

class EntityBiped(Entity):
    def __init__(self, level, pos):
        super().__init__(level, pos)

        self.model = Model()
        self.view = ViewBiped()

        self.gun_cooldown = 0
        self.reload_speed = 2
        self.reload = True

        self.shoot_sound = controller.sounds["player_shoot"]
        self.click_sound = controller.sounds["click"]

        self.pos = pos
        self.vel = Vec(0, 0)

    def update(self):

        if self.reload:
            self.power += self.reload_speed
            if self.power > self.max_power:
                self.power = self.max_power
            if self.power == self.max_power:
                self.reload = False
                self.gun_cooldown = 0

        return super().update()

    def walk(self, direction):
        super().walk(direction)

        self.view.walk_frame += self.view.facing * direction

    def shoot(self):

        if self.gun_cooldown == 0:
            if self.power >= 40 and not self.reload: ## TODO - these magic numbers are gunPower
                controller.sound_ctrl.play_sound(self.shoot_sound)
                bulletspeed = 20
                self.gun_cooldown = 20
                self.level.projectiles.append(Bullet(*self.view.held_pos.screen_coords(), self.view.aim, bulletspeed, self))
                self.power -= 40 ## TODO - magic number
                if self.power < 40:
                    self.reload = True

                return True
            else:
                controller.sound_ctrl.play_sound(self.click_sound)
                self.gun_cooldown = 30
                return False

    def render(self, camera_pos):

        ## TODO more logic to decide if sounds should be played... or maybe volume/pan control?
        if (self.view.walk_frame == 10 or self.view.walk_frame == 25) and self.touching_platform:
            controller.sound_ctrl.play_sound(controller.sounds["step%i"%(randint(1, 3))])

        super().render(camera_pos)
