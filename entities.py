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

shoaldier = {1: {}, -1: {}}
globalTextures = {1: {}, -1: {}}
def loadEntityTextures(scale, textures):
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

def blitRotateCenter(surf, image, angle, pos, camPos):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect().center)

    surf.blit(rotated_image, (new_rect.topleft[0] + pos[0] - camPos[0], new_rect.topleft[1] + pos[1] + camPos[1]))

class Shoaldier:
    def __init__(self, level, x, y):
        self.level = level
        self.player = level.player
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
    def tick(self, scale):
        self.x += self.xVel
        self.y += self.yVel
        
        self.get_touching(self.level, scale)
        if not self.touchingPlatform:
            self.yVel -= self.level.gravity #fix wall climbing

        if time()%2<0.1 and self.touchingPlatform and self.jumping == 0 and False:
            self.jumping = 1
            self.yVel += 10
            
        return True
    def draw(self, camX, camY, scale, win, mouseX, mouseY, winW, winH):
        head_rot = -math.degrees(math.atan2(self.y-self.player.y, self.player.x-self.x))
        head_rot_left = math.degrees(math.atan2(self.y-self.player.y, self.x-self.player.x))
        self.rightArm = (Sin((time()+1)*40)*10)-90-(5*self.facing)#head_rot-(15*self.facing)#
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
            blitRotateCenter(win, shoaldier[self.facing]['arm_far'], self.rightArm+180, (self.x-(14*scale),-self.y+(0*scale)), (camX,camY))
            handX = (self.x-(29*scale))+(Cos(-(self.rightArm))*(13*scale))
            handY = (-self.y-(2*scale))+(Sin(-(self.rightArm))*(13*scale))
            self.gunX = (handX+(8*scale))+(Cos(-(self.rightArm-self.rightHand))*(15*scale))
            self.gunY = handY+(Sin(-(self.rightArm-self.rightHand))*(15*scale))
            blitRotateCenter(win, shoaldier[self.facing]['gun_hand'], (self.rightArm-self.rightHand)+180, (handX,handY), (camX,camY))
        elif self.facing == 1:
            blitRotateCenter(win, shoaldier[self.facing]['arm_far'], self.leftArm, (self.x+(3*scale),-self.y+(0*scale)), (camX,camY))
            handX = (self.x-(4*scale))+(Cos(-self.leftArm)*(13*scale))
            handY = (-self.y-(2*scale))+(Sin(-self.leftArm)*(13*scale))
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
            headX = self.x-(6*scale)
            headY = -self.y-(19*scale)
            blitRotateCenter(win, shoaldier[self.facing]['head'], min(max(head_rot_left, -45), 45), (headX, headY), (camX,camY))
            blitRotateCenter(win, shoaldier[self.facing]['jaw'], min(max(head_rot_left, -45), 45), (headX-(2*scale), headY+(14*scale)), (camX,camY))
            blitRotateCenter(win, shoaldier[self.facing]['hat'], min(max(head_rot_left, -45), 45), (headX, headY-(10*scale)), (camX,camY))
            
        elif self.facing == 1:       
            headX = self.x-(4*scale)
            headY = -self.y-(19*scale)
            blitRotateCenter(win, shoaldier[self.facing]['head'], min(max(head_rot, -45), 45), (headX, headY), (camX,camY))          
            blitRotateCenter(win, shoaldier[self.facing]['jaw'], min(max(head_rot, -45), 45), (headX-(2*scale), headY+(14*scale)), (camX,camY))
            blitRotateCenter(win, shoaldier[self.facing]['hat'], min(max(head_rot, -45), 45), (headX, headY-(10*scale)), (camX,camY))
                

        if self.facing == -1:
            blitRotateCenter(win, shoaldier[self.facing]['arm_near'], self.leftArm+180, (self.x+(6*scale),-self.y+(0*scale)), (camX,camY))
            handX = (self.x-(5*scale))+(Cos(-(self.leftArm))*(13*scale))
            handY = (-(self.y+(2*scale)))+(Sin(-(self.leftArm))*(13*scale))
            blitRotateCenter(win, shoaldier[self.facing]['hand_near'], (self.leftArm-self.leftHand)+180, (handX,handY), (camX,camY))
        elif self.facing == 1:
            blitRotateCenter(win, shoaldier[self.facing]['arm_near'], self.rightArm, (self.x-(12*scale),-self.y+(0*scale)), (camX,camY))
            handX = (self.x-(29*scale))+(Cos(-self.rightArm)*(13*scale))
            handY = (-self.y-(1*scale))+(Sin(-self.rightArm)*(13*scale))
            self.gunX = (handX+(8*scale))+(Cos(-(self.rightArm+self.rightHand))*(15*scale))
            self.gunY = handY+(Sin(-(self.rightArm+self.rightHand))*(15*scale))
            blitRotateCenter(win, shoaldier[self.facing]['gun_hand'], self.rightArm+self.rightHand, (handX,handY), (camX,camY))
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
