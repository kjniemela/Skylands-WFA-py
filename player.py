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
    
    walkRight = [pygame.image.load('assets/body_walk%s.png' % frame) for frame in range(1, 9)]
    walkLeft = [pygame.transform.flip(pygame.image.load('assets/body_walk%s.png' % frame), True, False) for frame in range(1, 9)]
    idleRight = pygame.image.load('assets/body_idle.png')
    idleLeft = pygame.transform.flip(idleRight, True, False)
    headRight = pygame.image.load('assets/head.png')
    headLeft = pygame.transform.flip(headRight, True, False)

    armNearRight = pygame.image.load('assets/arm_near.png')
    armNearLeft = pygame.transform.flip(armNearRight, False, True)
    armFarRight = pygame.image.load('assets/arm_far.png')
    armFarLeft = pygame.transform.flip(armFarRight, False, True)

    handNearRight = pygame.image.load('assets/hand_near.png')
    handNearLeft = pygame.transform.flip(handNearRight, False, True)
    handFarRight = pygame.image.load('assets/hand_far.png')
    handFarLeft = pygame.transform.flip(handFarRight, False, True)

    GDFSERRight = pygame.image.load('assets/GDFSER.png')
    GDFSERLeft = pygame.transform.flip(GDFSERRight, False, True)
    
    powerBar = pygame.image.load('assets/power.png')
    healthBar = pygame.image.load('assets/health.png')

    gem = [pygame.image.load('assets/gem%s.png' % frame) for frame in range(1, 10)]

def drawHUD(win, player, fonts):
    win.blit(healthBar, (435-(142*(player.hp/player.maxHp)), 28))
    win.blit(powerBar, (333+(110*(player.gunCooldown/20)), 40))     
    win.blit(gem[int((time()*16)%9)], (10, 10))
    win.blit(fonts["gemCount"].render('x%d' % (player.gems), True, (91, 183, 0)) , (50, 22))

class Player:
    def __init__(self, x, y):
        self.level = None
        self.x = x
        self.y = y
        self.spawnpoint = (x, y)
        self.width = 40
        self.height = 60
        self.xVel = 0
        self.yVel = 0
        self.walkFrame = 0
        self.facing = 1
        self.touchingPlatform = False
        self.jumping = 0
        self.falling = True
        self.rightArm = 0
        self.leftArm = 0
        self.rightHand = 0
        self.leftHand = 0
        self.gunX = 0
        self.gunY = 0
        self.gunCooldown = 0

        self.gems = 0
        
        self.hp = 10
        self.maxHp = 10
    def draw(self, camX, camY, win, mouseX, mouseY, winW, winH):
        head_rot = -math.degrees(math.atan2(mouseY-((winH/2)+(50)), mouseX-(winW/2)))
        head_rot_left = math.degrees(math.atan2(mouseY-(((winH/2)+(50))), (winW/2)-mouseX))
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
        self.__init__(*self.spawnpoint)
    def check_inside(self, x, y):
        if self.x<x and self.x+(40)>x and self.y+(18)>y and self.y-(48)<y:
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
            self.x+(40)>platform.x and\
            self.y+(18)>platform.y-platform.h and\
            self.y-(48)<platform.y:
                self.touchingPlatform = True
                self.rightTouching = (self.x+(40))-platform.x
                self.leftTouching = (platform.x+platform.w)-self.x
                self.upTouching = (self.y+(18))-(platform.y-platform.h)
                self.downTouching = platform.y-(self.y-(48))
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

class Bullet:
    def __init__(self, x, y, d, speed, owner):
        self.x = x
        self.y = y
        self.d = d
        self.owner = owner
        self.xVel = (Cos(d)*(speed))#+owner.xVel
        self.yVel = (Sin(d)*(speed))#+owner.yVel
        self.age = 0
    def tick(self):
        self.x += self.xVel
        self.y += self.yVel
        self.age += 1
        #self.yVel -= 1
        return 0 < self.age < 100
    def get_touching(self, level):
        self.touchingPlatform = False
        self.rightTouching = 0
        self.leftTouching = 0
        self.upTouching = 0
        self.downTouching = 0
        for platform in level.platforms:
            if self.x+self.xVel<platform.x+platform.w and\
            self.x+self.xVel>platform.x and\
            self.y+self.yVel>platform.y-platform.h and\
            self.y+self.yVel<platform.y:
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
