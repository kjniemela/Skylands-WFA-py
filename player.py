from time import time
import math

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

def loadPlayerTextures(scale):
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
    
    walkRight = [pygame.transform.scale(pygame.image.load('assets/body_walk%s.png' % frame), (40*scale, 50*scale)) for frame in range(1, 9)]
    walkLeft = [pygame.transform.scale(pygame.transform.flip(pygame.image.load('assets/body_walk%s.png' % frame), True, False), (40*scale, 50*scale)) for frame in range(1, 9)]
    idleRight = pygame.transform.scale(pygame.image.load('assets/body_idle.png'), (40*scale, 50*scale))
    idleLeft = pygame.transform.flip(idleRight, True, False)
    headRight = pygame.transform.scale(pygame.image.load('assets/head.png'), (40*scale, 38*scale))
    headLeft = pygame.transform.flip(headRight, True, False)

    armNearRight = pygame.transform.scale(pygame.image.load('assets/arm_near.png'), (19*scale, 11*scale))
    armNearLeft = pygame.transform.flip(armNearRight, False, True)
    armFarRight = pygame.transform.scale(pygame.image.load('assets/arm_far.png'), (19*scale, 11*scale))
    armFarLeft = pygame.transform.flip(armFarRight, False, True)

    handNearRight = pygame.transform.scale(pygame.image.load('assets/hand_near.png'), (35*scale, 9*scale))
    handNearLeft = pygame.transform.flip(handNearRight, False, True)
    handFarRight = pygame.transform.scale(pygame.image.load('assets/hand_far.png'), (35*scale, 9*scale))
    handFarLeft = pygame.transform.flip(handFarRight, False, True)

    GDFSERRight = pygame.transform.scale(pygame.image.load('assets/GDFSER.png'), (23*scale, 12*scale))
    GDFSERLeft = pygame.transform.flip(GDFSERRight, False, True)


class Player:
    def __init__(self, level, x, y):
        self.level = level
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.xVel = 0
        self.yVel = 0
        self.walkFrame = 0
        self.facing = 1
        self.touchingPlatform = False
        self.jumping = 0
        self.rightArm = 0
        self.leftArm = 0
        self.rightHand = 0
        self.leftHand = 0
        self.gunX = 0
        self.gunY = 0
        self.gunCooldown = 0
    def draw(self, camX, camY, scale, win, mouseX, mouseY, winW, winH):
        head_rot = -math.degrees(math.atan2(mouseY-((winH/2)+(4*scale)), mouseX-(winW/2)))
        head_rot_left = math.degrees(math.atan2(mouseY-(-self.y), self.x-mouseX))
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

        
        if self.facing == -1:
            blitRotateCenter(win, armFarLeft, self.rightArm, (self.x+(1*scale),-self.y-(2*scale)), (camX,camY))
            handX = (self.x-(8*scale))+(Cos(-self.rightArm)*(9*scale))
            handY = (-self.y-(0*scale))+(Sin(-self.rightArm)*(9*scale))
            self.gunX = (handX+(8*scale))+(Cos(-(self.rightArm-self.rightHand))*(15*scale))
            self.gunY = handY+(Sin(-(self.rightArm-self.rightHand))*(15*scale))
            blitRotateCenter(win, handFarLeft, self.rightArm-self.rightHand, (handX,handY), (camX,camY))
            blitRotateCenter(win, GDFSERLeft, self.rightArm-self.rightHand, (self.gunX,self.gunY), (camX,camY))
        elif self.facing == 1:
            blitRotateCenter(win, armFarRight, self.leftArm, (self.x+(20*scale),-self.y-(2*scale)), (camX,camY))
            handX = (self.x+(12*scale))+(Cos(-self.leftArm)*(9*scale))
            handY = (-self.y-(0*scale))+(Sin(-self.leftArm)*(9*scale))
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
            blitRotateCenter(win, headLeft, min(max(head_rot_left, -45), 45), (self.x,-self.y-(20*scale)), (camX,camY))
        elif self.facing == 1:
            blitRotateCenter(win, headRight, min(max(head_rot, -45), 45), (self.x,-self.y-(20*scale)), (camX,camY))

        if self.facing == -1:
            blitRotateCenter(win, armNearLeft, self.leftArm, (self.x+(21*scale),-self.y-(2*scale)), (camX,camY))
            handX = (self.x+(12*scale))+(Cos(-self.leftArm)*(9*scale))
            handY = (-self.y-(0*scale))+(Sin(-self.leftArm)*(9*scale))
            blitRotateCenter(win, handNearLeft, self.leftArm-self.leftHand, (handX,handY), (camX,camY))
        elif self.facing == 1:
            blitRotateCenter(win, armNearRight, self.rightArm, (self.x,-self.y-(2*scale)), (camX,camY))
            handX = (self.x-(8*scale))+(Cos(-self.rightArm)*(9*scale))
            handY = (-self.y-(0*scale))+(Sin(-self.rightArm)*(9*scale))
            self.gunX = (handX+(8*scale))+(Cos(-(self.rightArm+self.rightHand))*(15*scale))
            self.gunY = handY+(Sin(-(self.rightArm+self.rightHand))*(15*scale))
            blitRotateCenter(win, GDFSERRight, self.rightArm+self.rightHand, (self.gunX,self.gunY), (camX,camY))
            blitRotateCenter(win, handNearRight, self.rightArm+self.rightHand, (handX,handY), (camX,camY))
            
    def get_touching(self, level, scale):
        self.touchingPlatform = False
        self.rightTouching = 0
        self.leftTouching = 0
        self.upTouching = 0
        self.downTouching = 0
        for platform in level.platforms:
            if self.x<platform.x+platform.w and\
            self.x+(40*scale)>platform.x and\
            self.y+(18*scale)>platform.y-platform.h and\
            self.y-(48*scale)<platform.y:
                self.touchingPlatform = True
                self.rightTouching = (self.x+(40*scale))-platform.x
                self.leftTouching = (platform.x+platform.w)-self.x
                self.upTouching = (self.y+(18*scale))-(platform.y-platform.h)
                self.downTouching = platform.y-(self.y-(48*scale))
                if self.downTouching > 0 and self.downTouching <= -(self.yVel-1):
                    self.yVel = 0
                    self.y += math.ceil(self.downTouching)-1
                    self.jumping = 0
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
    def __init__(self, x, y, d, speed, owner, scale):
        self.x = x
        self.y = y
        self.d = d
        self.owner = owner
        self.xVel = (Cos(d)*(speed*scale))#+owner.xVel
        self.yVel = (Sin(d)*(speed*scale))#+owner.yVel
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
        return False
