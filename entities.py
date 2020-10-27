from time import time
import math

from player import Bullet

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

shoaldier = {1: {}, -1: {}}
globalTextures = {1: {}, -1: {}}
def loadEntityTextures(textures):
    global shoaldier
    global globalTextures

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
        shoaldier[1][i[0]] = pygame.image.load('assets/shoaldier/%s.png'%(i[0]))
        shoaldier[-1][i[0]] = pygame.transform.flip(shoaldier[1][i[0]], True, False)
def loadEntitySounds(vol):
    global shoaldier_fire

    shoaldier_fire = pygame.mixer.Sound("assets/GDFSER-fire2.wav")
    shoaldier_fire.set_volume(1*vol)

def blitRotateCenter(surf, image, angle, pos, camPos):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect().center)

    surf.blit(rotated_image, (new_rect.topleft[0] + pos[0] - camPos[0], new_rect.topleft[1] + pos[1] + camPos[1]))

class Entity:
    width = 1
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
    def get_touching(self, level):
        self.touchingPlatform = False
        self.rightTouching = 0
        self.leftTouching = 0
        self.upTouching = 0
        self.downTouching = 0
        self.falling = True
        for platform in level.platforms:
            if self.x<platform.x+platform.w and\
            self.x+(self.width)>platform.x and\
            self.y+(self.heightHead)>platform.y-platform.h and\
            self.y-(self.heightBody)<platform.y:
                self.touchingPlatform = True
                self.rightTouching = (self.x+(self.width))-platform.x
                self.leftTouching = (platform.x+platform.w)-self.x
                self.upTouching = (self.y+(self.heightHead))-(platform.y-platform.h)
                self.downTouching = platform.y-(self.y-(self.heightBody))
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
                if self.downTouching > 1 and self.leftTouching > 0 and self.leftTouching <= -self.xVel: #this needs to be the relative xVel between the player and the platform
                    self.xVel = 0
                    self.x += math.ceil(self.leftTouching)

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

        if time()%2<0.1 and self.touchingPlatform and self.jumping == 0 and False:
            self.jumping = 1
            self.yVel += 10
            
        if True and self.gunCooldown == 0:
            shoaldier_fire.play()
            self.level.projectiles.append(Bullet(self.gunX, -self.gunY, self.rightArm+(self.rightHand*self.facing), 5, self))
            self.gunCooldown = 100

        if self.gunCooldown > 0:
            self.gunCooldown -= 1
            
        return True
    def draw(self, camX, camY, win, mouseX, mouseY, winW, winH):
        head_rot = -math.degrees(math.atan2(self.y-self.player.y, self.player.x-self.x))
        head_rot_left = math.degrees(math.atan2(self.y-self.player.y, self.x-self.player.x))
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
