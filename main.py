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

from player import *
from level import *
from entities import *
loadPlayerTextures(scale)
loadLevelTextures(scale)
loadEntityTextures(scale)

cursor = pygame.transform.scale(pygame.image.load('assets/cursor.png'), (16*scale, 16*scale))

###SOUND###
vol = 0.1
playMusic = False

pygame.mixer.pre_init(44100, -16, 4, 512)
pygame.mixer.init()
if playMusic:
    pygame.mixer.init()
    menuMusic = pygame.mixer.Sound("assets/The Light - The Album Leaf.wav")
    gameMusic = pygame.mixer.Sound("assets/music.ogg")
    gameMusic.set_volume(0.4*vol)
    menuMusic.set_volume(1*vol)
GDFSER_shoot = pygame.mixer.Sound("assets/GDFSER-fire2.wav")
GDFSER_shoot.set_volume(1*vol)

clock = pygame.time.Clock()

def drawGameWindow():
    global gameState
    global player

    if gameState == "mainMenu":
        win.blit(bg, (0, 0))
        win.blit(menu, (menuXOffset, 0))
        win.blit(pl, (int(winW/2) - int(255*(winH/720)/2), winH*0.85))
    elif gameState == "inGame":
        win.fill((240, 240, 255))
        level.draw(camX, camY, scale, win, mouseX, mouseY, winW, winH)
        player.draw(camX, camY, scale, win, mouseX, mouseY, winW, winH)

        win.blit(cursor, (mouseX-(8*scale),mouseY-(8*scale)))
    
    pygame.display.update()

level = Level("level1", scale)
player = Player(level, 250, 50)

run = True
gameState = "mainMenu"
mouseX, mouseY = 0, 0
camX, camY = 0, 0
winW, winH = 500, 480
fpst = time()
fps = 0
FPS = 60

if playMusic:
    curChannel = menuMusic.play(-1)

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

    if keys[pygame.K_SPACE] or not playMusic:
        break

    drawGameWindow()
if playMusic:
    menuMusic.fadeout(1000)
if run:
    alpha = 255
    if playMusic:
        while alpha > 0 and curChannel.get_busy():
            clock.tick(60)
            if alpha > 0:
                alpha -= 20#4
            menu.set_alpha(alpha)
            drawGameWindow()
    else:
        while alpha > 0:
            clock.tick(60)
            if alpha > 0:
                alpha -= 20#4
            menu.set_alpha(alpha)
            drawGameWindow()
    gameState = "inGame"
    if playMusic:
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

    player.get_touching(level, scale)

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
        player.yVel -= 1 #fix wall climbing
    
    if keys[pygame.K_w] and player.touchingPlatform and player.jumping == 0:
        player.jumping = 1
        player.yVel += 20
    if keys[pygame.K_s]:
        #player.yVel = 0
        player.yVel -= 1
    if keys[pygame.K_SPACE] and player.gunCooldown == 0:
        GDFSER_shoot.play()
        level.projectiles.append(Bullet(player.gunX, -player.gunY, player.rightArm+(player.rightHand*player.facing), 15, player, scale))
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
