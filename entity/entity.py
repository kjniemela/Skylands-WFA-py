from utils import *
from vec import Vec
from config import config
from window import controller

from entity.model import Model
from entity.view import View

class Entity:
    def __init__(self, pos):
        self.touching_platform = False
        self.falling = True
        self.jumping = 0

        self.model = Model()
        self.view = View()

        self.gun_cooldown = 0
        self.reload_speed = 2
        self.reload = True

        self.pos = pos
        self.spawnpoint = pos
        self.vel = Vec(0, 0)

        # HUD data
        self.hp = 10
        self.max_hp = 10
        self.power = 0
        self.max_power = 240

    def get_held_pos(self):
        return self.view.held_pos

    def get_hitbox(self):
        top_left = self.pos + Vec(self.model.x_offset, self.model.height_head)
        bottom_left = self.pos + Vec(self.model.x_offset, -self.model.height_body)
        top_right = top_left + Vec(self.model.width, 0)
        bottom_right = bottom_left + Vec(self.model.width, 0)

        return [
            top_left,
            top_right,
            bottom_right,
            bottom_left,
        ]

    def set_spawn(self, pos):
        self.pos = pos
        self.spawnpoint = pos

    def update(self):
        self.pos += self.vel

        ## TODO add animation logic here
        ## like "self.view.update()"

        return True

    def render(self, camera_pos):

        ## TODO more logic to decide if sounds should be played... or maybe volume/pan control?
        if (self.view.walk_frame == 10 or self.view.walk_frame == 25) and self.touching_platform:
            controller.sound_ctrl.play_sound(controller.sounds["step%i"%(randint(1, 3))])

        ## Render hitbox
        if config["debug"]:
            win = controller.win

            pygame.draw.rect(win, (0, 0, 0),
                (*((self.pos + Vec(self.model.x_offset, self.model.height_head) - camera_pos).screen_coords()),
                self.model.width, self.model.height_head + self.model.height_body))

        self.view.render(self.pos, camera_pos)

    def damage(self, dmg, src, knockback=Vec(0,0)):
        """
        0: fall damage - 1: melee damage
        """
        controller.sound_ctrl.play_sound(controller.sounds["hurt"])
        self.hp -= dmg
        self.vel += knockback

    def kill(self):
        level = self.level
        self.__init__(*self.spawnpoint, self.save_file)
        self.level = level

    def check_inside(self, pos):
        if self.x < pos.x and self.x + (self.width) > pos.x and self.y + (self.heightHead) > pos.y and self.y - (self.heightBody) < pos.y:
            return (True, (self.x + (self.width/2)) - pos.x, self.y - pos.y)
        else:
            return (False, 0, 0)

#     def get_colliding_platform(self, platform, down):
#         x3 = platform.x-((platform.w/2)*Cos(-platform.d))+((platform.h/2)*Sin(-platform.d))
#         y3 = platform.y+((platform.h/2)*Cos(-platform.d))+((platform.w/2)*Sin(-platform.d))
#         x4 = platform.x+((platform.w/2)*Cos(-platform.d))+((platform.h/2)*Sin(-platform.d))
#         y4 = platform.y+((platform.h/2)*Cos(-platform.d))-((platform.w/2)*Sin(-platform.d))
#         return self.get_colliding_lines(x3, y3, x4, y4, platform.d)

#     def get_colliding_lines(self, x3, y3, x4, y4, d, down=True):
#         if ((d+180)%360)-180 > 0:
#             col1 = line_collision((self.x+self.width+self.xOffset, self.y+(self.heightHead),
#                                    self.x+self.width+self.xOffset, self.y-(self.heightBody)),
#                              (x3, y3, x4, y4))
#             if not col1[0]:
#                 col1 = line_collision((self.x+self.xOffset, self.y+(self.heightHead),
#                                        self.x+self.xOffset, self.y-(self.heightBody)),
#                              (x3, y3, x4, y4))  
#         else:
#             col1 = line_collision((self.x+self.xOffset, self.y+(self.heightHead),
#                                    self.x+self.xOffset, self.y-(self.heightBody)),
#                              (x3, y3, x4, y4))
#             if not col1[0]:
#                 col1 = line_collision((self.x+self.width+self.xOffset, self.y+(self.heightHead),
#                                        self.x+self.width+self.xOffset, self.y-(self.heightBody)),
#                              (x3, y3, x4, y4))
#         col2 = line_collision((self.x+self.xOffset, self.y-(self.heightBody),
#                                self.x+self.width+self.xOffset, self.y-(self.heightBody)),
#                              (x3, y3, x4, y4))
        
#         #blitRotateCenter(self.win, headRight, 0, (x3, -y3), (camera_x,camera_y))
#         #blitRotateCenter(self.win, headRight, 0, (x4, -y4), (camera_x,camera_y))
#         #pygame.draw.aaline(self.win, (111, 255, 239, 0.5), (x3-camera_x, -(y3-camera_y)), (x4-camera_x, -(y4-camera_y)))
#         if col1[0]:
#             self.touchingPlatform = True
#             #blitRotateCenter(self.win, headRight, 0, (col[1],-col[2]), (camera_x,camera_y))
#             self.downTouching = col1[2]-(self.y-(self.heightBody))
#         if col2[0]:
#             self.touchingPlatform = True
#             #blitRotateCenter(self.win, headRight, 0, (col2[1],-col2[2]), (camera_x,camera_y))
#             if ((d+180)%360)-180 > 0:
#                 self.rightTouching = (self.x+self.width+self.xOffset)-col2[1]
#             else:
#                 self.leftTouching = col2[1]-self.x
#         return col1[0] if down else col2[0]

#     def get_touching(self, level, controlsMap, xOld, yOld):
#         self.rightTouching = 0
#         self.leftTouching = 0
#         self.upTouching = 0
#         self.downTouching = 0
#         self.falling = True
#         self.touchingPlatform = False

#         xChange = self.xVel
#         yChange = self.yVel

#         for platform in level.platforms:
#             if platform.d == 0:
#                 if self.x+self.xOffset<platform.x+(platform.w/2) and\
#                 self.x+(self.width+self.xOffset)>platform.x-(platform.w/2) and\
#                 self.y+(self.heightHead)>platform.y-(platform.h/2) and\
#                 self.y-(self.heightBody)<platform.y+(platform.h/2):
#                     self.touchingPlatform = True
#                     self.rightTouching = (self.x+(self.width+self.xOffset))-(platform.x-(platform.w/2))
#                     self.leftTouching = (platform.x+(platform.w/2))-(self.x+self.xOffset)
#                     self.upTouching = (self.y+(self.heightHead))-(platform.y-(platform.h/2))
#                     self.downTouching = (platform.y+(platform.h/2))-(self.y-(self.heightBody))

#                     if self.downTouching > 0 and self.downTouching <= -(yChange-2):
#                         if self.yVel < -5:
#                             controller.sound_ctrl.play_sound(controller.sounds["land"])

#                         if self.yVel < -20:
#                             dmg = math.ceil((abs(self.yVel)-11)/8)
#                             self.yVel = 0
#                             self.damage(dmg, 0) #FALL DAMAGE
#                         else:
#                             self.yVel = 0

#                         self.y += math.ceil(self.downTouching)-1
#                         self.jumping = 0
#                         self.falling = False

#                     if self.upTouching > 0 and self.upTouching <= yChange:
#                         self.yVel = 0
#                         self.y -= math.ceil(self.upTouching)
#                         #self.yChange -= math.ceil(self.upTouching)

#                     if self.downTouching > 1 and self.rightTouching > 0 and self.rightTouching <= self.xVel+((self.xOffset+self.width)-(self.lastXOffset+self.lastWidth)): #this needs to be the relative xVel between the player and the platform
#                         self.xVel = 0
#                         self.x -= math.ceil(self.rightTouching)
            
#                         if self.downTouching < 6:
#                             self.y += self.downTouching

#                         if controlsMap["left"] and (not self.walljump or self.wallJumpTime > 40):
#                             self.xVel = -4
#                             self.yVel = 10
#                             self.walljump = True
#                             self.falling = True
#                             self.wallJumpTime = 0
# ##                    elif self.downTouching > 1 and self.rightTouching > 0 and self.rightTouching <= self.xVel+((self.xOffset+self.width)-(self.lastXOffset+self.lastWidth)):
# ##                        self.xVel = 0
# ##                        self.xOffset = self.lastXOffset
# ##                        self.width = self.lastWidth
#                     if self.downTouching > 1 and self.leftTouching > 0 and self.leftTouching <= (-self.xVel)+(self.lastXOffset-self.xOffset): #this needs to be the relative xVel between the player and the platform
#                         self.xVel = 0
#                         self.x += math.ceil(self.leftTouching)
#                         if self.downTouching < 6:
#                             self.y += self.downTouching
#                         if controlsMap["right"] and (not self.walljump or self.wallJumpTime > 40):
#                             self.xVel = 4
#                             self.yVel = 10
#                             self.walljump = True
#                             self.falling = True                  
#                             self.wallJumpTime = 0
# ##                    elif self.downTouching > 1 and self.leftTouching > 0 and self.leftTouching <= (-self.xVel)+(self.lastXOffset-self.xOffset):
# ##                        self.xVel = 0
# ##                        self.xOffset = self.lastXOffset
#             else:
#                 if self.get_colliding_platform(platform, True):
#                     if self.downTouching > 0:
#                         if self.yVel < -20:
#                             dmg = math.ceil((abs(self.yVel)-11)/8)
#                             self.yVel = 0
#                             self.damage(dmg, 0) #FALL DAMAGE
#                         else:
#                             self.yVel += 0

#                         self.y += self.downTouching-1
#                         self.jumping = 0
#                         self.falling = False

#                 xVel = self.xVel
#                 self.x += xVel

#                 if self.get_colliding_platform(platform, False):
#                     if self.downTouching > 0 and self.leftTouching > 0:
#                         if self.downTouching < 6:
#                             self.y += self.downTouching
#                         else:
#                             self.x += math.ceil(self.leftTouching)
#                     if self.downTouching > 0 and self.rightTouching > 0:
#                         if self.downTouching < 6:
#                             self.y += self.downTouching
#                         else:
#                             self.x -= math.ceil(self.rightTouching)
#                 self.x -= xVel
#         self.lastXOffset = self.xOffset
#         self.lastWidth = self.width

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
    def tick(self):
        self.x += self.xVel
        self.y += self.yVel
        self.age += 1
        #self.yVel -= 1
        return 0 < self.age < 100

    def check_forward(self, pr, platform):
        if self.x+(self.xVel*pr)<platform.x+(platform.w/2) and\
            self.x+(self.xVel*pr)>platform.x-(platform.w/2) and\
            self.y+(self.yVel*pr)>platform.y-(platform.h/2) and\
            self.y+(self.yVel*pr)<platform.y+(platform.h/2):
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
                if self.x<platform.x+(platform.w/2) and\
                    self.x>platform.x-(platform.w/2) and\
                    self.y>platform.y-(platform.h/2) and\
                    self.y<platform.y+(platform.h/2):

                    return True
                elif distance(self.x, self.y, platform.x, platform.y)<=max(platform.w,platform.h):
                    pr = -1
                    while abs(pr*self.speed)>2:
                        pr *= 0.9
                        if self.check_forward(pr, platform):
                            return True
            else:
                x3 = platform.x-((platform.w/2)*Cos(-platform.d))+((platform.h/2)*Sin(-platform.d))
                y3 = platform.y+((platform.h/2)*Cos(-platform.d))+((platform.w/2)*Sin(-platform.d))
                x4 = platform.x+((platform.w/2)*Cos(-platform.d))+((platform.h/2)*Sin(-platform.d))
                y4 = platform.y+((platform.h/2)*Cos(-platform.d))-((platform.w/2)*Sin(-platform.d))
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