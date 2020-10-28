from time import time
import sys
import os
try:
    import pygame
except ModuleNotFoundError:
    print("ModuleNotFoundError: Pygame module could not be found.")
    if input("Install pygame [y/n]? ").lower() == "y":
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        import pygame
    else:
        exit()

if len(sys.argv) > 1:
    save_file = sys.argv[1]
else:
    save_file = None

print(save_file)

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 2
    
pygame.display.init()
islandIcon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(islandIcon)

window = pygame.display.set_mode((960, 720), pygame.RESIZABLE)
win = pygame.Surface((480, 360))

pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

pygame.display.set_caption("Skylands %d.%d.%d" % (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH))

asciiIcon = """                   
         %%%%@  *@@@            
      *##################       
    ######################(     
 ###########################@###
  ,,,,,,,##########,,,*,,,,,&,,#
   ,,,,,,,,,,,,#,,,,,,,,,,,,%,, 
     ,,,,,,,,,,,,,,,,,,,,,,,%,  
      ,,,,,,,,,,,,,,,,,,,,,,#   
      .,,,,,,,,,,,,,,,,,,,,,(   
        ,,,,,,,,,,,,,,,,,,, @   
           ,,,,,,,,,,,,,,.  @   
            .,  ,,,,,,,,,   @   
                ,,,,,,,,    @   
                  ,,,,          
                   , .     
"""

menuXOffset = 0

#MENU
sky = pygame.image.load('assets/sky.png').convert_alpha()
menuIsland = pygame.image.load('assets/menu.png').convert()
loading = pygame.image.load('assets/loading.png')
playText = pygame.image.load('assets/play.png')

bg = pygame.transform.scale(sky, (480, 360))
menu = pygame.transform.scale(menuIsland, (480, 360))
pl = playText

win.blit(bg, (0, 0))
win.blit(menu, (menuXOffset, 0))
win.blit(loading, (15, 660))
pygame.display.update()

###TEXTURES###
#HUD
HUD = pygame.image.load('assets/HUD.png')
HUD_back = pygame.image.load('assets/HUD back.png')

#ITEMS
STBRight = pygame.image.load('assets/STB Mk1.png')
STBLeft = pygame.transform.flip(STBRight, False, True)

items = {1: {
        'stb': STBRight
    }, -1: {
        'stb': STBLeft
        }}

from player import *
from level import *
loadPlayerTextures()
loadLevelTextures()
loadEntityTextures(items)

cursor = pygame.image.load('assets/cursor.png')
##############

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

loadEntitySounds(vol)
###########

###FONTS###
pygame.font.init()
fonts = {
    "gemCount": pygame.font.Font('freesansbold.ttf', 16),
    "achievementTitle": pygame.font.Font('C:\\WINDOWS\\Fonts\\Inkfree.ttf', 15),
    "achievementSubt": pygame.font.Font('C:\\WINDOWS\\Fonts\\Inkfree.ttf', 6),
    }
###########

clock = pygame.time.Clock()

def drawGameWindow():
    global gameState
    global player
    global fonts

    zoom = 1 #make global or smth later

    if gameState == "mainMenu" or gameState == "fade":
        if gameState == "fade":
            win.blit(bg, (0, 0))
        win.blit(menu, (0, 0))
        if gameState == "mainMenu":
            win.blit(pl, (176, 306))
    elif gameState == "inGame":
        win.fill((240, 240, 255))
        level.draw(camX, camY, win, mouseX, mouseY, winW, winH)
        player.draw(camX, camY, win, mouseX, mouseY, winW, winH)

        win.blit(HUD_back, (293, 28))
        drawHUD(win, player, fonts)
        win.blit(HUD, (0, 0))

        level.achievement_handler.draw(win, level, fonts)

        win.blit(cursor, ((mouseX-(8*(winW/480)))//(winW/480),(mouseY-(8*(winH/360)))//(winH/360)))
        
    #window.blit(pygame.transform.scale(win, (winW, winH)), (menuXOffset,0))
    window.blit(pygame.transform.scale(win, (winW*zoom, winH*zoom)), (menuXOffset-(winW*(0.5*(zoom-1))),-(winW*(0.5*(zoom-1)))))
    pygame.display.update()

player = Player(125, 25, save_file)
level = Level("level1", player)

print(asciiIcon)
print("Skylands: Worlds from Above v%d.%d.%d" % (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH))

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
            winW, winH = int(480*(event.h/360)), event.h
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            bg = pygame.transform.scale(sky, (event.w, event.h))
            menu = pygame.transform.scale(menuIsland, (480, 360))
            pl = pygame.transform.scale(playText, (127, 20))
            menuXOffset = int(event.w/2) - int(480*(event.h/360)/2)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or not playMusic:
        break

    drawGameWindow()
if playMusic:
    menuMusic.fadeout(1000)
if run:
    gameState = "fade"
    alpha = 255
    if playMusic:
        while alpha > 0 or curChannel.get_busy():
            clock.tick(60)
            if alpha > 0:
                alpha -= 6
            menu.set_alpha(alpha)
            drawGameWindow()
    else:
        while alpha > 0:
            clock.tick(60)
            if alpha > 0:
                alpha -= 20
            menu.set_alpha(alpha)
            drawGameWindow()
    gameState = "inGame"
    if playMusic:
        gameMusic.play(-1)
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if not save_file == None:
                player.save()
            run = False
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
            mouseX -= menuXOffset
        if event.type == pygame.VIDEORESIZE:
            winW, winH = int(480*(event.h/360)), event.h
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            #bg = pygame.transform.scale(sky, (event.w, event.h))
            #menu = pygame.transform.scale(menuIsland, (480, 360))
            pl = pygame.transform.scale(playText, (int(255*(event.h/720)), int(event.h/18)))
            menuXOffset = int(event.w/2) - int(960*(event.h/720)/2)

    keys = pygame.key.get_pressed()

    player.x += player.xVel
    player.y += player.yVel

    player.get_touching(level)

    if keys[pygame.K_a]:
        player.xVel -= 2
        player.walkFrame += player.facing*-1
        #player.facing = -1
    if keys[pygame.K_d]:
        player.xVel += 2
        player.walkFrame += player.facing
        #player.facing = 1

    player.xVel *= 0.6
    if abs(player.xVel) < 0.01:
        player.xVel = 0
    if player.falling:
        player.yVel -= level.gravity
    
    if keys[pygame.K_w] and player.touchingPlatform and player.jumping == 0:
        player.jumping = 1
        player.yVel += 10
    if keys[pygame.K_s]:
        player.yVel = 0
        #player.yVel -= 1
    if keys[pygame.K_SPACE] and player.gunCooldown == 0:
        GDFSER_shoot.play()
        level.projectiles.append(Bullet(player.gunX, -player.gunY, player.rightArm+(player.rightHand*player.facing), 20, player))
        player.gunCooldown = 30

    if player.gunCooldown > 0:
        player.gunCooldown -= 1

    if player.y < -2000:
        player.hp = 0

    if player.hp <= 0:
        player.kill()
        level.achievement_handler.trigger("StillAlive")

    camX += (((player.x+5)-(480/2))-camX)*0.2
    camY += (((player.y+20)+(360/2))-camY)*0.2

    drawGameWindow()
    
    fps += 1
    if time() - fpst > 1:
        fpst = time()
        FPS = fps
        fps = 0
    pygame.display.set_caption("Skylands    FPS: %d X: %d Y: %d" % (FPS, player.x, player.y))

pygame.quit()
