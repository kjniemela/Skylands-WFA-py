from utils import *
from vec import Vec
from window import controller

from entity.biped import EntityBiped

class Player(EntityBiped):

    textures = controller.player_textures

    def __init__(self, level, pos):
        super().__init__(level, pos)
        
        self.spawnpoint = Vec(*pos)
        self.walljump = False
        self.wallJumpTime = 0
        self.quest = "B116"
        self.gems = 0

        print(self.textures)

    def set_spawn(self, pos):
        self.pos = pos
        self.spawnpoint = Vec(*pos)

    # def save(self):
    #     with open(self.save_file, mode='w') as f:
    #         data = [
    #             str("SAVENAME"),
    #             str(self.x),
    #             str(self.y),
    #             str(self.xVel),
    #             str(self.yVel),
    #             str(self.gunCooldown),
    #             str(self.gems),
    #             str(self.hp),
    #             str(self.maxHp),
    #             ]
    #         f.write('\n'.join(data))

    def kill(self):
        super().kill()

        self.__init__(self.level, self.spawnpoint)

    def update(self):
        super().update()

        controls = self.level.game.controls

        mouse_x, mouse_y = controller.mouse_pos
        self.view.aim = -math.degrees(math.atan2(mouse_y-(180+24), mouse_x-(240+16)))

        if not (self.walljump and self.wallJumpTime < 5):
            if controls["left"]:
                self.walk(-1)
                if not self.touching_platform: self.vel.x *= 0.648

            if controls["right"]:
                self.walk(1)
                if not self.touching_platform: self.vel.x *= 0.648

        if self.walljump and not self.falling:
            self.walljump = False
            self.wallJumpTime = 0
        elif self.walljump:
            self.wallJumpTime += 1

        if abs(self.vel.x) < 0.01:
            self.vel.x = 0

        if False: ## FLIGHT CHECK HERE TODO ?? - this would be the cheat-flying mode for debugging, maybe remove?
            if keys[controlsMap["up"]]:
                self.yVel = 5
            elif keys[controlsMap["sneak"]]:
                self.yVel = -5
            elif not  keys[pygame.K_g]:
                self.yVel *= 0.9
        else:
            if controls["jump"]:
                self.jump(Vec(0, 10))
            elif self.touching_platform:
                if controls["sneak"] and not self.falling:
                    self.sneak()
                elif self.view.states["sneaking"]:
                    self.unsneak()
                    
        if controls["reset"]:
            # self.kill()
            self.level.__init__(self.level.game, self.level.level_name, controller.sounds)
            self.level.set_player(self)
            self.level.start()
        
        if controls["shoot"]:
            self.shoot()

        if controls["reload"] and self.gun_cooldown == 0:
                self.reload = True

        if self.pos.y < -2000:
            self.hp = 0

        if self.hp <= 0:
            self.kill()
            self.level.game.achievement_handler.trigger("StillAlive")

        return True

    def render(self, camera_pos):
        super().render(camera_pos)
