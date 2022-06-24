from utils import *
from vec import Vec
from config import config
from window import controller

from entity.biped import EntityBiped
from entity.model.base import Model
from entity.view.shoaldier import ViewShoaldier
from world.projectile import Bullet

## TODO - probably add a EntityEnemy class in between these?
class EntityShoaldier(EntityBiped):
    def __init__(self, level, pos):
        super().__init__(level, pos)

        self.view = ViewShoaldier()

        self.shoot_sound = controller.sounds["player_shoot"]

    def update(self):

        aim_vec = self.level.player.pos - self.pos
        self.view.aim = -math.degrees(math.atan2(*aim_vec)) + 90

        if self.gun_cooldown == 0:
            self.shoot()

        return super().update()

    # def render(self, camera_pos):
    #     super().render(camera_pos)
