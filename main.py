import math

def Sin(x):
    return math.sin(math.radians(x))
def Cos(x):
    return math.cos(math.radians(x))

from time import time
try:
    import pygame
except ModuleNotFoundError:
    print("ModuleNotFoundError: Pygame module could not be found.")
    t=time()
    while time()-t<1:
        pass
    exit()
pygame.display.init()
islandIcon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(islandIcon)

win = pygame.display.set_mode((960, 720), pygame.RESIZABLE)

pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

pygame.display.set_caption("Skylands")

scale = 2
menuXOffset = 0

###TEXTURES###

#BACKGROUND
sky = pygame.image.load('assets/sky.png').convert_alpha()
menuIsland = pygame.image.load('assets/menu.png').convert()
loading = pygame.image.load('assets/loading.png')
playText = pygame.image.load('assets/play.png')


bg = sky
menu = menuIsland
pl = playText

win.blit(bg, (0, 0))
win.blit(menu, (menuXOffset, 0))
win.blit(loading, (15, 660))
pygame.display.update()

#PLATFORMS
platformTextures = {
    "ground1": pygame.image.load('assets/ground1.png')
    }

#PLAYER
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
bullet = pygame.transform.scale(pygame.image.load('assets/GDFSER-bullet.png'), (int(26*scale/2), int(12*scale/2)))

cursor = pygame.transform.scale(pygame.image.load('assets/cursor.png'), (16*scale, 16*scale))

###SOUND###
vol = 0.1

pygame.mixer.init()
menuMusic = pygame.mixer.Sound("assets/The Light - The Album Leaf.wav")
gameMusic = pygame.mixer.Sound("assets/music.ogg")
gameMusic.set_volume(0.4*vol)
menuMusic.set_volume(1*vol)
curChannel = menuMusic.play(-1)

clock = pygame.time.Clock()

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
    def draw(self, camX, camY):
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
            
    def get_touching(self, level):
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
                if player.downTouching > 0 and player.downTouching <= -(self.yVel-1):
                    player.yVel = 0
                    player.y += math.ceil(player.downTouching)-1
                    player.jumping = 0
                if player.upTouching > 0 and player.upTouching <= self.yVel:
                    player.yVel = 0
                    player.y -= math.ceil(player.upTouching)
                if player.rightTouching > 0 and player.rightTouching <= self.xVel: #this needs to be the relative xVel between the player and the platform
                    player.xVel = 0
                    player.x -= math.ceil(player.rightTouching)
                if player.leftTouching > 0 and player.leftTouching <= -self.xVel: #this needs to be the relative xVel between the player and the platform
                    player.xVel = 0
                    player.x += math.ceil(player.leftTouching)

class Bullet:
    def __init__(self, x, y, d, speed, owner):
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

class Level:
    def __init__(self, src):

        self.platforms = []
        self.projectiles = []
        
        f = open("levels/"+src)
        data = f.read().split("\n")
        f.close()
        data = [i.split(" ") for i in data]
        for i in data:
            if i[1] == '1':
                self.platforms.append(Platform(i[0], int(i[2]), int(i[3]), int(i[4]), int(i[5])))
    def draw(self, camX, camY):
        for platform in self.platforms:
            win.blit(platform.texture, (platform.x-camX, -(platform.y-camY)))
        for projectile in self.projectiles:
            if projectile.tick() and not projectile.get_touching(self):
                blitRotateCenter(win, bullet, projectile.d, (projectile.x,-projectile.y), (camX,camY))
            else:
                del self.projectiles[self.projectiles.index(projectile)]

class Platform:
    def __init__(self, texture, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.texture = platformTextures[texture]

def blitRotateCenter(surf, image, angle, pos, camPos):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect().center)

    surf.blit(rotated_image, (new_rect.topleft[0] + pos[0] - camPos[0], new_rect.topleft[1] + pos[1] + camPos[1]))

def drawGameWindow():
    global gameState
    global player
    #win.blit(bg, (0, 0))
    win.fill((240, 240, 255))

    if gameState == "mainMenu":
        win.blit(menu, (menuXOffset, 0))
        win.blit(pl, (int(winW/2) - int(255*(winH/720)/2), winH*0.85))
    elif gameState == "inGame":
        level.draw(camX, camY)
        player.draw(camX, camY)

    win.blit(cursor, (mouseX-(8*scale),mouseY-(8*scale)))
    
    pygame.display.update()

level = Level("level1")
player = Player(level, 250, 50)

run = True
gameState = "mainMenu"
mouseX, mouseY = 0, 0
camX, camY = 0, 0
winW, winH = 500, 480
fpst = time()
fps = 0
FPS = 60
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
        if event.type == pygame.VIDEORESIZE:
            winW, winH = event.w, event.h
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            bg = pygame.transform.scale(sky, (event.w, event.h))
            menu = pygame.transform.scale(menuIsland, (int(960*(event.h/720)), event.h))
            pl = pygame.transform.scale(playText, (int(255*(event.h/720)), int(event.h/18)))
            menuXOffset = int(winW/2) - int(960*(winH/720)/2)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:# or True:
        break

    drawGameWindow()
menuMusic.fadeout(1000)
if run:
    alpha = 255
    while alpha > 0 and curChannel.get_busy():
        clock.tick(60)
        if alpha > 0:
            alpha -= 20#4
        menu.set_alpha(alpha)
        drawGameWindow()
    gameState = "inGame"
    gameMusic.play(-1)
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
        if event.type == pygame.VIDEORESIZE:
            winW, winH = event.w, event.h
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            bg = pygame.transform.scale(sky, (event.w, event.h))
            menu = pygame.transform.scale(menuIsland, (int(960*(event.h/720)), event.h))
            pl = pygame.transform.scale(playText, (int(255*(event.h/720)), int(event.h/18)))
            menuXOffset = int(winW/2) - int(960*(winH/720)/2)

    keys = pygame.key.get_pressed()

    player.x += player.xVel
    player.y += player.yVel

    player.get_touching(level)

    if keys[pygame.K_a]:
        player.xVel -= 4
        player.walkFrame += player.facing*-1
        #player.facing = -1
    elif keys[pygame.K_d]:
        player.xVel += 4
        player.walkFrame += player.facing
        #player.facing = 1

    player.xVel *= 0.6
    if abs(player.xVel) < 0.01:
        player.xVel = 0
    if not player.touchingPlatform:
        player.yVel -= 1
    
    if keys[pygame.K_w] and player.touchingPlatform and player.jumping == 0:
        player.jumping = 1
        player.yVel += 20
    if keys[pygame.K_s]:
        #player.yVel = 0
        player.yVel -= 1
    if keys[pygame.K_SPACE] and player.gunCooldown == 0:
        level.projectiles.append(Bullet(player.gunX, -player.gunY, player.rightArm+(player.rightHand*player.facing), 15, player))
        player.gunCooldown = 20

    if player.gunCooldown > 0:
        player.gunCooldown -= 1

    camX += ((player.x-(winW/2))-camX)*0.2
    camY += ((player.y+(winH/2))-camY)*0.2

    drawGameWindow()
    
    fps += 1
    if time() - fpst > 1:
        fpst = time()
        FPS = fps
        fps = 0
    pygame.display.set_caption("Skylands    FPS: %d" % (FPS))

pygame.quit()
