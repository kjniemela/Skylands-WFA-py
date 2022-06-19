from utils import *
from vec import Vec
from window import controller

from entity.biped import EntityBiped

class Player(EntityBiped):
    def __init__(self, pos):
        super().__init__(pos)
        
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

        self.__init__(self.spawnpoint)

    # def update(self):
    #     return super().update()

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