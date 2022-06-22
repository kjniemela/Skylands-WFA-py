from utils import *
from vec import Vec
from window import controller

from entity.biped import EntityBiped

class Player(EntityBiped):
    def __init__(self, level, pos):
        super().__init__(level, pos)

        self.level = level
        
        self.spawnpoint = Vec(*pos)
        self.walljump = False
        self.wallJumpTime = 0
        self.quest = "B116"
        self.gems = 0

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

        ## TODO - MAKE RESPAWNING WORK AGAIN!
        self.__init__(self.level, self.spawnpoint)

    def update(self):
        super().update()

        controls = self.level.game.controls

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

        if self.touching_platform:
            self.vel.x *= 0.6
        else:
            self.vel.x *= 0.925

        if abs(self.vel.x) < 0.01:
            self.vel.x = 0

        if False: ## FLIGHT CHECK HERE TODO ??
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
            self.kill()
            self.level.__init__(self.level.game, self.level.level_name, controller.sounds)
            self.level.set_player(self)
            self.level.start()
        
        if controls["shoot"] and self.gun_cooldown == 0:
            if self.power >= 40 and not self.reload: ## TODO - these magic numbers are gunPower
                controller.sound_ctrl.play_sound(controller.sounds["player_shoot"])
                bulletspeed = 20
                self.gun_cooldown = 20
                self.level.projectiles.append(Bullet(*self.view.held_pos, self.view.aim, bulletspeed, self))
                self.power -= 40 ## TODO - magic number
                if self.power < 40:
                    self.reload = True
            else:
                controller.sound_ctrl.play_sound(controller.sounds["click"])
                self.gun_cooldown = 30

        if self.gun_cooldown > 0:
            self.gun_cooldown -= 1
        if controls["reload"] and self.gun_cooldown == 0:
                self.reload = True

        if self.reload:
            self.power += self.reload_speed
            if self.power > self.max_power:
                self.power = self.max_power
            if self.power == self.max_power:
                self.reload = False
                self.gun_cooldown = 0

        if self.pos.y < -2000:
            self.hp = 0

        if self.hp <= 0:
            self.kill()
            self.level.game.achievement_handler.trigger("StillAlive")

        return True

    def render(self, camera_pos):
        super().render(camera_pos)

class Bullet:
    def __init__(self, x, y, d, speed, owner):
        self.x = x
        self.y = y
        self.d = d
        self.owner = owner
        self.xVel = (Cos(d)*(speed))#+owner.xVel
        self.yVel = (Sin(d)*(speed))#+owner.yVel
        self.speed = speed
        self.age = 0

    def update(self):
        self.x += self.xVel
        self.y += self.yVel
        self.age += 1
        #self.yVel -= 1

        return 0 < self.age < 100

    def check_forward(self, pr, platform):
        if (
            self.x + (self.xVel*pr) < platform.x + (platform.w/2) and
            self.x + (self.xVel*pr) > platform.x - (platform.w/2) and
            self.y + (self.yVel*pr) > platform.y - (platform.h/2) and
            self.y + (self.yVel*pr) < platform.y + (platform.h/2)
        ):
            return True
        else:
            return False

    def get_touching(self, level):
        self.touchingPlatform = False
        self.rightTouching = 0
        self.leftTouching = 0
        self.upTouching = 0
        self.downTouching = 0

        for platform in level.platforms:
            if platform.d == 0:
                if (
                    self.x < platform.x + (platform.w/2) and
                    self.x > platform.x - (platform.w/2) and
                    self.y > platform.y - (platform.h/2) and
                    self.y < platform.y + (platform.h/2)
                ):
                    return True
                elif distance(self.x, self.y, platform.x, platform.y)<=max(platform.w,platform.h):
                    pr = -1

                    while abs(pr*self.speed)>2:
                        pr *= 0.9

                        if self.check_forward(pr, platform):
                            return True
            else:
                x3 = platform.x - ((platform.w/2) * Cos(-platform.d)) + ((platform.h/2) * Sin(-platform.d))
                y3 = platform.y + ((platform.h/2) * Cos(-platform.d)) + ((platform.w/2) * Sin(-platform.d))
                x4 = platform.x + ((platform.w/2) * Cos(-platform.d)) + ((platform.h/2) * Sin(-platform.d))
                y4 = platform.y + ((platform.h/2) * Cos(-platform.d)) - ((platform.w/2) * Sin(-platform.d))
                col = line_collision((self.x, self.y, self.x-self.xVel, self.y-self.yVel),
                                     (x3, y3, x4, y4))
                if col[0]:
                    return True

        for entity in level.entities:
            if not entity == self.owner:
                hit, xD, yD = entity.check_inside(self.x, self.y)
                if hit:
                    #print(hit, xD, yD)
                    entity.damage(1, 2, (self.xVel*0.2, self.yVel*0.2 + 1))
                    return True
        if not level.player == self.owner:
            hit, xD, yD = level.player.check_inside(self.x, self.y)
            if hit:
                level.player.damage(1, 2, (self.xVel*1, self.yVel*1 + 1))
                return True
        return False