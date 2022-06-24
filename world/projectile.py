from utils import *

class Bullet:
    def __init__(self, pos, d, speed, owner):
        self.pos = pos
        self.d = d
        self.owner = owner
        self.vel = Vec(
            (Cos(d)*(speed)),
            (Sin(d)*(speed))
        )
        self.age = 0

    def update(self):
        self.pos += self.vel
        self.age += 1
        #self.vel.y -= self.owner.level.gravity

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