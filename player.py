from time import time
import math

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

from collision import *

import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def blitRotateCenter(surf, image, angle, pos, camPos):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect().center)

    surf.blit(rotated_image, (new_rect.topleft[0] + pos[0] - camPos[0], new_rect.topleft[1] + pos[1] + camPos[1]))

def loadPlayerTextures():
    global walkRight
    global walkLeft
    global idleRight
    global idleLeft
    global headRight
    global headLeft
    global armNearRight
    global armNearLeft
    global armFarRight
    global armFarLeft
    global handNearRight
    global handNearLeft
    global handFarRight
    global handFarLeft
    global GDFSERRight
    global GDFSERLeft
    global powerBar
    global healthBar
    global gem
    
    walkRight = [pygame.image.load(resource_path('assets/body_walk%s.png' % frame)) for frame in range(1, 9)]
    walkLeft = [pygame.transform.flip(pygame.image.load(resource_path('assets/body_walk%s.png' % frame)), True, False) for frame in range(1, 9)]
    idleRight = pygame.image.load(resource_path('assets/body_idle.png'))
    idleLeft = pygame.transform.flip(idleRight, True, False)
    headRight = pygame.image.load(resource_path('assets/head.png'))
    headLeft = pygame.transform.flip(headRight, True, False)

    armNearRight = pygame.image.load(resource_path('assets/arm_near.png'))
    armNearLeft = pygame.transform.flip(armNearRight, False, True)
    armFarRight = pygame.image.load(resource_path('assets/arm_far.png'))
    armFarLeft = pygame.transform.flip(armFarRight, False, True)

    handNearRight = pygame.image.load(resource_path('assets/hand_near.png'))
    handNearLeft = pygame.transform.flip(handNearRight, False, True)
    handFarRight = pygame.image.load(resource_path('assets/hand_far.png'))
    handFarLeft = pygame.transform.flip(handFarRight, False, True)

    GDFSERRight = pygame.image.load(resource_path('assets/GDFSER.png'))
    GDFSERLeft = pygame.transform.flip(GDFSERRight, False, True)
    
    powerBar = pygame.image.load(resource_path('assets/power.png'))
    healthBar = pygame.image.load(resource_path('assets/health.png'))

    gem = [pygame.image.load(resource_path('assets/gem%s.png' % frame)) for frame in range(1, 10)]

def drawHUD(win, player, fonts):
    win.blit(healthBar, (435-(142*(player.hp/player.maxHp)), 28))
    win.blit(powerBar, (333+(110*(player.gunCooldown/20)), 40))     
    win.blit(gem[int((time()*16)%9)], (10, 10))
    win.blit(fonts["gemCount"].render('x%d' % (player.gems), True, (91, 183, 0)) , (50, 22))

class Player:
    def __init__(self, x, y, save_file):
        self.save_file = save_file
        self.spawnpoint = (x, y)
        self.xOffset = 0
        self.width = 40
        self.lastXOffset = 0
        self.lastWidth = 0
        self.heightHead = 18
        self.heightBody = 48
        self.walkFrame = 0
        self.facing = 1
        self.touchingPlatform = False
        self.falling = True
        self.jumping = 0
        self.walljump = False
        self.wallJumpTime = 0
        self.gunX = 0
        self.gunY = 0
        self.level = None
        self.rightArm = 0
        self.leftArm = 0
        self.rightHand = 0
        self.leftHand = 0
        self.gunCooldown = 120
        if save_file == None:
            self.x = x
            self.y = y
            self.xVel = 0
            self.yVel = 0

            self.gems = 0
            
            self.hp = 10
            self.maxHp = 10
        else:
            self.load(self.save_file)
    def set_spawn(self, x, y):
        self.x = x
        self.y = y
        self.spawnpoint = (x, y)
    def load(self, save_file):
        with open(save_file) as f:
            data = f.read().split('\n')
        print(data)
        self.x = float(data[1])
        self.y = float(data[2])
        self.xVel = float(data[3])
        self.yVel = float(data[4])
        #self.gunCooldown = int(data[5])
        self.gems = int(data[6])
        self.hp = int(data[7])
        self.maxHp = int(data[8])
    def save(self):
        with open(self.save_file, mode='w') as f:
            data = [
                str("SAVENAME"),
                str(self.x),
                str(self.y),
                str(self.xVel),
                str(self.yVel),
                str(self.gunCooldown),
                str(self.gems),
                str(self.hp),
                str(self.maxHp),
                ]
            f.write('\n'.join(data))
    def draw(self, camX, camY, win, mouseX, mouseY, winW, winH):
        if not self.level == None:
            if self.level.debugMode:
                pygame.draw.rect(win, (0, 0, 0),
                                 ((self.x+self.xOffset)-camX, -((self.y+self.heightHead)-camY),
                                  self.width, self.heightHead+self.heightBody))
        head_rot = -math.degrees(math.atan2(mouseY-(180+24), mouseX-(240+16)))
        head_rot_left = ((360+(head_rot))%360)-180#math.degrees(math.atan2(mouseY-(180+15), 240-mouseX))
        self.rightArm = head_rot-(15*self.facing)#(Sin((time()+1)*40)*10)-90-(5*self.facing)#
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

        #arm position is a bit buggy
        
        if self.facing == -1:
            blitRotateCenter(win, armFarLeft, self.rightArm, (self.x-(3),-self.y-(2)), (camX,camY))
            handX = (self.x-(8))+(Cos(-self.rightArm)*(11))
            handY = (-self.y-(0))+(Sin(-self.rightArm)*(11))
            self.gunX = (handX+(8))+(Cos(-(self.rightArm-self.rightHand))*(15))
            self.gunY = handY+(Sin(-(self.rightArm-self.rightHand))*(16))
            blitRotateCenter(win, handFarLeft, self.rightArm-self.rightHand, (handX,handY), (camX,camY))
            blitRotateCenter(win, GDFSERLeft, self.rightArm-self.rightHand, (self.gunX,self.gunY), (camX,camY))
        elif self.facing == 1:
            blitRotateCenter(win, armFarRight, self.leftArm, (self.x+(15),-self.y-(2)), (camX,camY))
            handX = (self.x+(11))+(Cos(-self.leftArm)*(11))
            handY = (-self.y-(0))+(Sin(-self.leftArm)*(11))
            blitRotateCenter(win, handFarRight, self.leftArm+self.leftHand, (handX,handY), (camX,camY))

        if abs(self.xVel) > 0:
            if self.facing < 0:
                win.blit(walkLeft[self.walkFrame//4], (self.x-camX,-(self.y-camY)))
            elif self.facing > 0:
                win.blit(walkRight[self.walkFrame//4], (self.x-camX,-(self.y-camY)))
        else:
            if self.facing == -1:
                win.blit(idleLeft, (self.x-camX,-(self.y-camY)))
            elif self.facing == 1:
                win.blit(idleRight, (self.x-camX,-(self.y-camY)))

        if self.facing == -1:
            blitRotateCenter(win, headLeft, min(max(head_rot_left, -45), 45), (self.x,-self.y-(20)), (camX,camY))
        elif self.facing == 1:
            blitRotateCenter(win, headRight, min(max(head_rot, -45), 45), (self.x,-self.y-(20)), (camX,camY))

        if self.facing == -1:
            blitRotateCenter(win, armNearLeft, self.leftArm, (self.x+17,-self.y-0), (camX,camY))
            handX = (self.x+(12))+(Cos(-self.leftArm)*(11))
            handY = (-self.y-(0))+(Sin(-self.leftArm)*(11))
            blitRotateCenter(win, handNearLeft, self.leftArm-self.leftHand, (handX,handY), (camX,camY))
        elif self.facing == 1:
            blitRotateCenter(win, armNearRight, self.rightArm, (self.x-2,-self.y-(2)), (camX,camY))
            handX = (self.x-(8))+(Cos(-self.rightArm)*(11))
            handY = (-self.y-(0))+(Sin(-self.rightArm)*(11))
            self.gunX = (handX+(8))+(Cos(-(self.rightArm+self.rightHand))*(15))
            self.gunY = handY+(Sin(-(self.rightArm+self.rightHand))*(16))
            blitRotateCenter(win, GDFSERRight, self.rightArm+self.rightHand, (self.gunX,self.gunY), (camX,camY))
            blitRotateCenter(win, handNearRight, self.rightArm+self.rightHand, (handX,handY), (camX,camY))
    def damage(self, dmg, src, knockback=(0,0)):
        """
        0: fall damage - 1: melee damage
        """
        self.hp -= dmg
        self.xVel += knockback[0]
        self.yVel += knockback[1]
    def kill(self):
        self.__init__(*self.spawnpoint, self.save_file)
    def check_inside(self, x, y):
        if self.x<x and self.x+(self.width)>x and self.y+(self.heightHead)>y and self.y-(self.heightBody)<y:
            return (True, (self.x+(self.width/2))-x, self.y-y)
        else:
            return (False, 0, 0)
    def get_colliding_platform(self, platform, down):
        x3 = platform.x-((platform.w/2)*Cos(-platform.d))+((platform.h/2)*Sin(-platform.d))
        y3 = platform.y+((platform.h/2)*Cos(-platform.d))+((platform.w/2)*Sin(-platform.d))
        x4 = platform.x+((platform.w/2)*Cos(-platform.d))+((platform.h/2)*Sin(-platform.d))
        y4 = platform.y+((platform.h/2)*Cos(-platform.d))-((platform.w/2)*Sin(-platform.d))
        return self.get_colliding_lines(x3, y3, x4, y4, platform.d)
    def get_colliding_lines(self, x3, y3, x4, y4, d, down=True):
        if ((d+180)%360)-180 > 0:
            col1 = line_collision((self.x+self.width+self.xOffset, self.y+(self.heightHead),
                                   self.x+self.width+self.xOffset, self.y-(self.heightBody)),
                             (x3, y3, x4, y4))
            if not col1[0]:
                col1 = line_collision((self.x+self.xOffset, self.y+(self.heightHead),
                                       self.x+self.xOffset, self.y-(self.heightBody)),
                             (x3, y3, x4, y4))  
        else:
            col1 = line_collision((self.x+self.xOffset, self.y+(self.heightHead),
                                   self.x+self.xOffset, self.y-(self.heightBody)),
                             (x3, y3, x4, y4))
            if not col1[0]:
                col1 = line_collision((self.x+self.width+self.xOffset, self.y+(self.heightHead),
                                       self.x+self.width+self.xOffset, self.y-(self.heightBody)),
                             (x3, y3, x4, y4))
        col2 = line_collision((self.x+self.xOffset, self.y-(self.heightBody),
                               self.x+self.width+self.xOffset, self.y-(self.heightBody)),
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
                self.rightTouching = (self.x+self.width+self.xOffset)-col2[1]
            else:
                self.leftTouching = col2[1]-self.x
        return col1[0] if down else col2[0]
    def get_touching(self, level, controlsMap, keys):
        self.rightTouching = 0
        self.leftTouching = 0
        self.upTouching = 0
        self.downTouching = 0
        self.falling = True
        self.touchingPlatform = False
        for platform in level.platforms:
            if platform.d == 0:
                if self.x+self.xOffset<platform.x+(platform.w/2) and\
                self.x+(self.width+self.xOffset)>platform.x-(platform.w/2) and\
                self.y+(self.heightHead)>platform.y-(platform.h/2) and\
                self.y-(self.heightBody)<platform.y+(platform.h/2):
                    self.touchingPlatform = True
                    self.rightTouching = (self.x+(self.width+self.xOffset))-(platform.x-(platform.w/2))
                    self.leftTouching = (platform.x+(platform.w/2))-(self.x+self.xOffset)
                    self.upTouching = (self.y+(self.heightHead))-(platform.y-(platform.h/2))
                    self.downTouching = (platform.y+(platform.h/2))-(self.y-(self.heightBody))
                    if self.downTouching > 0 and self.downTouching <= -(self.yVel-2):
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
                    if self.downTouching > 1 and self.rightTouching > 0 and self.rightTouching <= self.xVel+((self.xOffset+self.width)-(self.lastXOffset+self.lastWidth)): #this needs to be the relative xVel between the player and the platform
                        self.xVel = 0
                        self.x -= math.ceil(self.rightTouching)
                        if self.downTouching < 6:
                            self.y += self.downTouching
                        if keys[controlsMap["left"]] and (not self.walljump or self.wallJumpTime > 50):
                            self.xVel = -5
                            self.yVel = 10
                            self.walljump = True
                            self.falling = True
                            self.wallJumpTime = 0
                            print(self.downTouching)
##                    elif self.downTouching > 1 and self.rightTouching > 0 and self.rightTouching <= self.xVel+((self.xOffset+self.width)-(self.lastXOffset+self.lastWidth)):
##                        self.xVel = 0
##                        self.xOffset = self.lastXOffset
##                        self.width = self.lastWidth
                    if self.downTouching > 1 and self.leftTouching > 0 and self.leftTouching <= (-self.xVel)+(self.lastXOffset-self.xOffset): #this needs to be the relative xVel between the player and the platform
                        self.xVel = 0
                        self.x += math.ceil(self.leftTouching)
                        if self.downTouching < 6:
                            self.y += self.downTouching
                        if keys[controlsMap["right"]] and (not self.walljump or self.wallJumpTime > 50):
                            self.xVel = 5
                            self.yVel = 10
                            self.walljump = True
                            self.falling = True                  
                            self.wallJumpTime = 0
##                    elif self.downTouching > 1 and self.leftTouching > 0 and self.leftTouching <= (-self.xVel)+(self.lastXOffset-self.xOffset):
##                        self.xVel = 0
##                        self.xOffset = self.lastXOffset
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
        self.lastXOffset = self.xOffset
        self.lastWidth = self.width

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
        for polyplat in level.polyplats:
            for i in range(len(polyplat.points)):# if polyplat.points[(i+1)%len(polyplat.points)][1]>polyplat.points[i][1] else -1
                col = line_collision((self.x, self.y, self.x-self.xVel, self.y-self.yVel),
                                     (*polyplat.points[i], *polyplat.points[(i+1)%len(polyplat.points)]))
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
