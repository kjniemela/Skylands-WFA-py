from time import time
import math
import os
import sys

from player import Bullet
from collision import *

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def Sin(x):
    return math.sin(math.radians(x))
def Cos(x):
    return math.cos(math.radians(x))
try:
    import pygame
except ModuleNotFoundError:
    print("ModuleNotFoundError: Pygame module could not be found.")
    t=time()
    while time()-t<1:
        pass
    exit()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

shoaldier = {1: {}, -1: {}}
door_controller = None
globalTextures = {1: {}, -1: {}}
def loadEntityTextures(textures):
    global shoaldier
    global globalTextures
    global door_controller

    globalTextures = textures

    shoaldierTextures = [
        ('arm_far', 32, 10),
        ('arm_near', 28, 12),
        ('foot_far', 16, 14),
        ('foot_near', 16, 14),
        ('hand_far', 46, 16),
        ('hand_near', 50, 16),
        ('hat', 32, 60),
        ('head', 32, 40),
        ('jaw', 36, 11),
        ('leg_far', 16, 6),
        ('leg_near', 16, 6),
        ('torso', 22, 30),
        ('gun_hand', 62, 14)
    ]
    for i in shoaldierTextures:
        shoaldier[1][i[0]] = pygame.image.load(resource_path('assets/shoaldier/%s.png'%(i[0])))
        shoaldier[-1][i[0]] = pygame.transform.flip(shoaldier[1][i[0]], True, False)
    door_controller = pygame.image.load(resource_path('assets/door_controller.png'))
def loadEntitySounds(vol):
    global shoaldier_fire

    shoaldier_fire = pygame.mixer.Sound(resource_path("assets/GDFSER-fire2.wav"))
    shoaldier_fire.set_volume(1*vol)

def blitRotateCenter(surf, image, angle, pos, camPos):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect().center)

    surf.blit(rotated_image, (new_rect.topleft[0] + pos[0] - camPos[0], new_rect.topleft[1] + pos[1] + camPos[1]))

class Entity:
    width = 1
    xOffset = 0
    heightHead = 1
    heightBody = 1
    xVel = 0
    yVel = 0
    facing = 1
    touchingPlatform = False
    jumping = 0
    falling = True
    kills = 0
    hp = 1
    is_dead = False
    aim_target = 0
    aim = 0
    brain = {}
    def __init__(self, level, x, y):
        self.level = level
        self.player = level.player
        self.x = x
        self.y = y
    def tick(self):
        if self.hp <= 0:
            self.kill()
        if self.is_dead:
            return False
        else:
            return True
    def damage(self, dmg, src, knockback=(0,0)):
        """
        0: fall damage - 1: melee damage
        """
        self.hp -= dmg
        self.xVel += knockback[0]
        self.yVel += knockback[1]
    def kill(self):
        self.is_dead = True
    def check_inside(self, x, y):
        if self.x<x and self.x+(self.width)>x and self.y+(self.heightHead)>y and self.y-(self.heightBody)<y:
            return (True, (self.x+(self.width/2))-x, self.y-y)
        else:
            return (False, 0, 0)
    def can_see(self, target):
        for platform in self.level.platforms:
            if platform.collides_with_line(self.x, self.y, target.x, target.y):
                return False
        return True
    def get_colliding_platform(self, platform, down):
        x3 = platform.x-((platform.w/2)*Cos(-platform.d))+((platform.h/2)*Sin(-platform.d))
        y3 = platform.y+((platform.h/2)*Cos(-platform.d))+((platform.w/2)*Sin(-platform.d))
        x4 = platform.x+((platform.w/2)*Cos(-platform.d))+((platform.h/2)*Sin(-platform.d))
        y4 = platform.y+((platform.h/2)*Cos(-platform.d))-((platform.w/2)*Sin(-platform.d))
        return self.get_colliding_lines(x3, y3, x4, y4, platform.d)
    def get_colliding_lines(self, x3, y3, x4, y4, d, down=True):
        if ((d+180)%360)-180 > 0:
            col1 = line_collision((self.x+self.width, self.y+(self.heightHead), self.x+self.width, self.y-(self.heightBody)),
                             (x3, y3, x4, y4))
            if not col1[0]:
                col1 = line_collision((self.x, self.y+(self.heightHead), self.x, self.y-(self.heightBody)),
                             (x3, y3, x4, y4))  
        else:
            col1 = line_collision((self.x, self.y+(self.heightHead), self.x, self.y-(self.heightBody)),
                             (x3, y3, x4, y4))
            if not col1[0]:
                col1 = line_collision((self.x+self.width, self.y+(self.heightHead), self.x+self.width, self.y-(self.heightBody)),
                             (x3, y3, x4, y4))
        col2 = line_collision((self.x, self.y-(self.heightBody), self.x+(self.width), self.y-(self.heightBody)),
                             (x3, y3, x4, y4))
        
        #blitRotateCenter(self.win, headRight, 0, (x3, -y3), (camX,camY))
        #blitRotateCenter(self.win, headRight, 0, (x4, -y4), (camX,camY))
        #pygame.draw.aaline(self.win, (111, 255, 239, 0.5), (x3-camX, -(y3-camY)), (x4-camX, -(y4-camY)))
        if col1[0]:
            self.touchingPlatform = True
            #blitRotateCenter(self.win, headRight, 0, (col[1],-col[2]), (camX,camY))
            self.downTouching = col1[2]-(self.y-(self.heightBody))
        if col2[0]:
            self.touchingPlatform = True
            #blitRotateCenter(self.win, headRight, 0, (col2[1],-col2[2]), (camX,camY))
            if ((d+180)%360)-180 > 0:
                self.rightTouching = (self.x+(self.width))-col2[1]
            else:
                self.leftTouching = col2[1]-self.x
        return col1[0] if down else col2[0]
    def get_touching(self, level):
        self.rightTouching = 0
        self.leftTouching = 0
        self.upTouching = 0
        self.downTouching = 0
        self.falling = True
        self.touchingPlatform = False
        for platform in level.platforms:
            if platform.d == 0:
                if self.x<platform.x+(platform.w/2) and\
                self.x+(40)>platform.x-(platform.w/2) and\
                self.y+(18)>platform.y-(platform.h/2) and\
                self.y-(48)<platform.y+(platform.h/2):
                    self.touchingPlatform = True
                    self.rightTouching = (self.x+(self.width))-(platform.x-(platform.w/2))
                    self.leftTouching = (platform.x+(platform.w/2))-self.x
                    self.upTouching = (self.y+(self.heightHead))-(platform.y-(platform.h/2))
                    self.downTouching = (platform.y+(platform.h/2))-(self.y-(self.heightBody))
                    if self.downTouching > 0 and self.downTouching <= -(self.yVel-1):
                        if self.yVel < -20:
                            dmg = math.ceil((abs(self.yVel)-11)/8)
                            self.yVel = 0
                            self.damage(dmg, 0) #FALL DAMAGE
                        else:
                            self.yVel = 0
                        self.y += math.ceil(self.downTouching)-1
                        self.jumping = 0
                        self.falling = False
                    if self.upTouching > 0 and self.upTouching <= self.yVel:
                        self.yVel = 0
                        self.y -= math.ceil(self.upTouching)
                    if self.downTouching > 1 and self.rightTouching > 0 and self.rightTouching <= self.xVel: #this needs to be the relative xVel between the player and the platform
                        self.xVel = 0
                        self.x -= math.ceil(self.rightTouching)
                        if self.downTouching < 6:
                            self.y += self.downTouching
                    if self.downTouching > 1 and self.leftTouching > 0 and self.leftTouching <= -self.xVel: #this needs to be the relative xVel between the player and the platform
                        self.xVel = 0
                        self.x += math.ceil(self.leftTouching)
                        if self.downTouching < 6:
                            self.y += self.downTouching
            else:
                if self.get_colliding_platform(platform, True):
                    if self.downTouching > 0:
                        if self.yVel < -20:
                            dmg = math.ceil((abs(self.yVel)-11)/8)
                            self.yVel = 0
                            self.damage(dmg, 0) #FALL DAMAGE
                        else:
                            self.yVel += 0
                        self.y += self.downTouching-1
                        self.jumping = 0
                        self.falling = False
                xVel = self.xVel
                self.x += xVel
                if self.get_colliding_platform(platform, False):
                    if self.downTouching > 0 and self.leftTouching > 0:
                        if self.downTouching < 6:
                            self.y += self.downTouching
                        else:
                            self.x += math.ceil(self.leftTouching)
                    if self.downTouching > 0 and self.rightTouching > 0:
                        if self.downTouching < 6:
                            self.y += self.downTouching
                        else:
                            self.x -= math.ceil(self.rightTouching)
                self.x -= xVel
        for polyplat in level.polyplats:
            for i in range(len(polyplat.points)):# 
                if self.get_colliding_lines(*polyplat.points[i], *polyplat.points[(i+1)%len(polyplat.points)],
                1 if polyplat.points[(i+1)%len(polyplat.points)][1]>polyplat.points[i][1] else -1, True):
                    if self.downTouching > 0:
                        if self.yVel < -20:
                            dmg = math.ceil((abs(self.yVel)-11)/8)
                            self.yVel = 0
                            self.damage(dmg, 0) #FALL DAMAGE
                        else:
                            self.yVel += 0
                        self.y += self.downTouching-1
                        self.jumping = 0
                        self.falling = False
                xVel = self.xVel
                self.x += xVel
                if self.get_colliding_lines(*polyplat.points[i], *polyplat.points[(i+1)%len(polyplat.points)],
                1, False):
                    if self.downTouching > 0 and self.leftTouching > 0:
                        if self.downTouching < 6:
                            self.y += self.downTouching
                        else:
                            self.x += math.ceil(self.leftTouching)
                    if self.downTouching > 0 and self.rightTouching > 0:
                        if self.downTouching < 6:
                            self.y += self.downTouching
                        else:
                            self.x -= math.ceil(self.rightTouching)
                self.x -= xVel
    def draw(self, camX, camY, win, mouseX, mouseY, winW, winH):
        if not self.level == None:
            if self.level.debugMode:
                pygame.draw.rect(win, (0, 0, 0),
                                 ((self.x+self.xOffset)-camX, -((self.y+self.heightHead)-camY),
                                  self.width, self.heightHead+self.heightBody))

class Shoaldier(Entity):
    def __init__(self, level, x, y):
        super().__init__(level, x, y)
        self.width = 40
        self.heightHead = 24
        self.heightBody = 48
        self.walkFrame = 0
        self.rightArm = 0
        self.leftArm = 0
        self.rightHand = 0
        self.leftHand = 0
        self.gunX = 0
        self.gunY = 0
        self.gunCooldown = 100
        self.hp = 3
        self.brain['fire'] = False
        self.brain['jump'] = False
    def tick(self):
        if not super().tick():
            return False
        self.x += self.xVel
        self.y += self.yVel
        
        self.get_touching(self.level)
        self.xVel *= 0.6
        if abs(self.xVel) < 0.01:
            self.xVel = 0
        if self.falling:
            self.yVel -= self.level.gravity

        if time()%2<0.1 and self.touchingPlatform and self.jumping == 0 and self.brain['jump']:
            self.jumping = 1
            self.yVel += 10
            
        if self.brain['fire'] and self.gunCooldown == 0:
            #shoaldier_fire.set_volume(1*vol)
            #shoaldier_fire.play()
            self.level.projectiles.append(Bullet(self.gunX, -self.gunY, self.rightArm+(self.rightHand*self.facing), 5, self))
            self.gunCooldown = 100

        if self.gunCooldown > 0:
            self.gunCooldown -= 1

        if self.can_see(self.player):
            self.aim_target = -math.degrees(math.atan2(self.y-self.player.y, self.player.x-self.x))
            self.brain['fire'] = True
        else:
            self.aim_target = 180
            self.brain['fire'] = False
        if abs(self.aim_target-self.aim) > 180:
            self.aim += ((self.aim_target%360)-(self.aim%360))*0.1
        else:
            self.aim += (self.aim_target-self.aim)*0.1
            
        return True
    def draw(self, camX, camY, win, mouseX, mouseY, winW, winH):
        super().draw(camX, camY, win, mouseX, mouseY, winW, winH)
        head_rot = self.aim
        head_rot_left = ((360+(head_rot))%360)-180
        self.rightArm = head_rot-(15*self.facing)
        self.leftArm = (Sin(time()*40)*10)-90-(5*self.facing)
        self.rightHand = 15
        self.leftHand = 10
        if abs(head_rot)> 90:
            self.facing = -1
        else:
            self.facing = 1
        
        if self.walkFrame + 1 >= 32:
            self.walkFrame = 0
        if self.walkFrame < 0:
            self.walkFrame = 30

        
        if self.facing == -1:
            blitRotateCenter(win, shoaldier[self.facing]['arm_far'], self.rightArm+180, (self.x-(14),-self.y+(0)), (camX,camY))
            handX = (self.x-(29))+(Cos(-(self.rightArm))*(13))
            handY = (-self.y-(2))+(Sin(-(self.rightArm))*(13))
            self.gunX = (handX+(28))+(Cos(-(self.rightArm-self.rightHand))*(15))
            self.gunY = handY+(Sin(-(self.rightArm-self.rightHand))*(15))+4
            blitRotateCenter(win, shoaldier[self.facing]['gun_hand'], (self.rightArm-self.rightHand)+180, (handX,handY), (camX,camY))
        elif self.facing == 1:
            blitRotateCenter(win, shoaldier[self.facing]['arm_far'], self.leftArm, (self.x+(3),-self.y+(0)), (camX,camY))
            handX = (self.x-(4))+(Cos(-self.leftArm)*(13))
            handY = (-self.y-(2))+(Sin(-self.leftArm)*(13))
            blitRotateCenter(win, shoaldier[self.facing]['hand_far'], self.leftArm+self.leftHand, (handX,handY), (camX,camY))

        if abs(self.xVel) > 0:
            if self.facing < 0:
                blitRotateCenter(win, shoaldier[self.facing]['torso'], 0, (self.x,-self.y), (camX,camY))
            elif self.facing > 0:
                blitRotateCenter(win, shoaldier[self.facing]['torso'], 0, (self.x,-self.y), (camX,camY))
        else:
            if self.facing == -1:
                blitRotateCenter(win, shoaldier[self.facing]['torso'], 0, (self.x,-self.y), (camX,camY))
            elif self.facing == 1:
                blitRotateCenter(win, shoaldier[self.facing]['torso'], 0, (self.x,-self.y), (camX,camY))

        if self.facing == -1:
            headX = self.x-(7)
            headY = -self.y-(19)
            blitRotateCenter(win, shoaldier[self.facing]['head'], min(max(head_rot_left, -45), 45), (headX, headY), (camX,camY))
            blitRotateCenter(win, shoaldier[self.facing]['jaw'], min(max(head_rot_left, -45), 45), (headX-(0), headY+(14)), (camX,camY))
            blitRotateCenter(win, shoaldier[self.facing]['hat'], min(max(head_rot_left, -45), 45), (headX, headY-(10)), (camX,camY))
            
        elif self.facing == 1:       
            headX = self.x-(3)
            headY = -self.y-(19)
            blitRotateCenter(win, shoaldier[self.facing]['head'], min(max(head_rot, -45), 45), (headX, headY), (camX,camY))          
            blitRotateCenter(win, shoaldier[self.facing]['jaw'], min(max(head_rot, -45), 45), (headX+(1), headY+(14)), (camX,camY))
            blitRotateCenter(win, shoaldier[self.facing]['hat'], min(max(head_rot, -45), 45), (headX, headY-(10)), (camX,camY))
                

        if self.facing == -1:
            blitRotateCenter(win, shoaldier[self.facing]['arm_near'], self.leftArm+180, (self.x+(6),-self.y+(0)), (camX,camY))
            handX = (self.x-(5))+(Cos(-(self.leftArm))*(13))
            handY = (-(self.y+(2)))+(Sin(-(self.leftArm))*(13))
            blitRotateCenter(win, shoaldier[self.facing]['hand_near'], (self.leftArm-self.leftHand)+180, (handX,handY), (camX,camY))
        elif self.facing == 1:
            blitRotateCenter(win, shoaldier[self.facing]['arm_near'], self.rightArm, (self.x-(12),-self.y+(0)), (camX,camY))
            handX = (self.x-(29))+(Cos(-self.rightArm)*(13))
            handY = (-self.y-(1))+(Sin(-self.rightArm)*(13))
            self.gunX = (handX+(28))+(Cos(-(self.rightArm+self.rightHand))*(15))
            self.gunY = handY+(Sin(-(self.rightArm+self.rightHand))*(15))+4
            blitRotateCenter(win, shoaldier[self.facing]['gun_hand'], self.rightArm+self.rightHand, (handX,handY), (camX,camY))
    def damage(self, dmg, src, knockback=(0,0)): #0: fall damage - 1: melee damage
        self.hp -= dmg

class DoorController(Entity):
    def __init__(self, level, x, y):
        super().__init__(level, x, y)
        self.width = 16
        self.heightHead = 0
        self.heightBody = 20
        self.hp = 1
    def tick(self):
        super().tick()
            
        return True
    def draw(self, camX, camY, win, mouseX, mouseY, winW, winH):
        super().draw(camX, camY, win, mouseX, mouseY, winW, winH)
        blitRotateCenter(win, door_controller, 0, (self.x,-self.y), (camX,camY))
    def damage(self, dmg, src, knockback=(0,0)): #0: fall damage - 1: melee damage
        self.hp -= dmg
