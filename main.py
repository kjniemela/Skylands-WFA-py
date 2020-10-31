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

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 6
    
pygame.display.init()
islandIcon = pygame.image.load(resource_path('assets/icon.png'))
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
sky = pygame.image.load(resource_path('assets/sky.png')).convert_alpha()
menuIsland = pygame.image.load(resource_path('assets/menu.png')).convert()
loading = pygame.image.load(resource_path('assets/loading.png'))
playText = pygame.image.load(resource_path('assets/play.png'))

bg = pygame.transform.scale(sky, (480, 360))
menu = pygame.transform.scale(menuIsland, (480, 360))
pl = playText

win.blit(bg, (0, 0))
win.blit(menu, (menuXOffset, 0))
win.blit(loading, (15, 660))
pygame.display.update()

###TEXTURES###
#PLAY MENU
playMenu = pygame.image.load(resource_path('assets/playMenu2.png'))
creditsSlide = pygame.image.load(resource_path('assets/credits.png'))

#HUD
HUD = pygame.image.load(resource_path('assets/HUD.png'))
HUD_back = pygame.image.load(resource_path('assets/HUD back.png'))

#ITEMS
STBRight = pygame.image.load(resource_path('assets/STB Mk1.png'))
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

cursor = pygame.image.load(resource_path('assets/cursor.png'))
##############

###SOUND###
vol = 0.25
playMusic = False

pygame.mixer.pre_init(44100, -16, 4, 512)
pygame.mixer.init()
if playMusic:
    pygame.mixer.init()
    menuMusic = pygame.mixer.Sound(resource_path("assets/The Light - The Album Leaf.wav"))
    gameMusic = pygame.mixer.Sound(resource_path("assets/music.ogg"))
    gameMusic.set_volume(0.4*vol)
    menuMusic.set_volume(1*vol)

GDFSER_shoot = pygame.mixer.Sound(resource_path("assets/GDFSER-fire2.wav"))
GDFSER_shoot.set_volume(1*vol)

loadEntitySounds(vol)
###########

###FONTS###
pygame.font.init()
fonts = {
    "gemCount": pygame.font.Font(pygame.font.match_font('arial', bold=1), 16),
    "achievementTitle": pygame.font.Font(pygame.font.match_font('inkfree'), 15),
    "achievementSubt": pygame.font.Font(pygame.font.match_font('inkfree'), 6),
    }
###########

###FADE###
class Fade:
    def __init__(self, fadeWhite, fadeBlack):
        self.fadeWhite = fadeWhite
        self.fadeBlack = fadeBlack
        self.alpha = 0
        self.active = False
        self.color = "black"
        self.speed = 1
        self.next_state = ""
        self.fading = True
    def fade_white(self, speed, next_state):
        self.color = "white"
        self.speed = speed
        self.next_state = next_state
        self.active = True
        self.fading = True
    def fade_black(self, speed, next_state):
        self.color = "black"
        self.speed = speed
        self.next_state = next_state
        self.active = True
        self.fading = True
    def draw(self, win):
        global gameState
        
        if self.active:
            if self.color == "white":
                self.fadeWhite.set_alpha(self.alpha)
                win.blit(self.fadeWhite, (0,0))
            elif self.color == "black":
                self.fadeBlack.set_alpha(self.alpha)
                win.blit(self.fadeBlack, (0,0))
            if self.fading:
                if self.alpha < 255:
                    self.alpha += self.speed
                else:
                    self.fading = False
                    gameState = self.next_state
            else:
                if self.alpha > 0:
                    self.alpha -= self.speed
                else:
                    self.active = False

fade = Fade(pygame.image.load(resource_path('assets/fadeWhite.png')).convert(),\
            pygame.image.load(resource_path('assets/fadeBlack.png')).convert())
##########

clock = pygame.time.Clock()
creditsY = 0

def drawGameWindow():
    global gameState
    global player
    global fonts
    global creditsY

    zoom = 1 #make global or smth later

    if gameState == "mainMenu" or gameState == "fade":
        if gameState == "fade":
            win.blit(bg, (0, 0))
        win.blit(menu, (0, 0))
        if gameState == "mainMenu":
            win.blit(pl, (176, 306))
    elif gameState == "playMenu":
        win.blit(playMenu, (0, 0))
        win.blit(cursor, (mouseX-8,mouseY-8))
    elif gameState == "credits":
        win.fill((251, 251, 254))
        win.blit(creditsSlide, (0, min(creditsY, 0)))
        creditsY -= 1
        if creditsY < -1440:
            fade.fade_white(6, "playMenu")
    elif gameState == "inGame":
        win.fill((240, 240, 255))
        level.draw(camX, camY, win, mouseX, mouseY, winW, winH)
        player.draw(camX, camY, win, mouseX, mouseY, winW, winH)
        level.draw_overlays(camX, camY, win, mouseX, mouseY, winW, winH)

        win.blit(HUD_back, (293, 28))
        drawHUD(win, player, fonts)
        win.blit(HUD, (0, 0))

        level.achievement_handler.draw(win, level, fonts)

        win.blit(cursor, (mouseX-8,mouseY-8))

    fade.draw(win)
    window.blit(pygame.transform.scale(win, (winW*zoom, winH*zoom)), (menuXOffset-(winW*(0.5*(zoom-1))),-(winW*(0.5*(zoom-1)))))
    pygame.display.update()

print(asciiIcon)
print("Skylands: Worlds from Above v%d.%d.%d" % (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH))

player = Player(125, 25, save_file)
level = Level("lab", player)

run = True
runMenu = True
gameState = "mainMenu"
mouseX, mouseY = 0, 0
camX, camY = ((player.x+5)-(480/2)), ((player.y+20)+(360/2))
winW, winH = 500, 480
fpst = time()
fps = 0
FPS = 60
fly = False

if playMusic:
    curChannel = menuMusic.play(-1)

    while run and runMenu:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = event.pos
                mouseX -= menuXOffset
                mouseX *= 480/winW
                mouseY *= 360/winH
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseX, mouseY = event.pos
                    mouseX -= menuXOffset
                    mouseX *= 480/winW
                    mouseY *= 360/winH
                    #print(mouseX, mouseY)
                    if gameState == "playMenu":
                        if mouseY<32 and 375<mouseX<470:
                            runMenu = False
                        if 47<mouseY<77 and 375<mouseX<470:
                            #LOAD
                            pass
                        if 125<mouseY<155 and 375<mouseX<470:
                            #SETTINGS
                            pass
                        if 310<mouseY<348 and 377<mouseX<465:
                            fade.fade_white(6, "mainMenu")
                        if 310<mouseY<348 and 16<mouseX<100:
                            creditsY = 40
                            fade.fade_white(6, "credits")
            if event.type == pygame.VIDEORESIZE:
                winW, winH = int(480*(event.h/360)), event.h
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                bg = pygame.transform.scale(sky, (event.w, event.h))
                menu = pygame.transform.scale(menuIsland, (480, 360))
                pl = pygame.transform.scale(playText, (127, 20))
                menuXOffset = int(event.w/2) - int(480*(event.h/360)/2)

        keys = pygame.key.get_pressed()

        if gameState == "mainMenu":
            if keys[pygame.K_SPACE]:
                fade.fade_white(6, "playMenu")

        drawGameWindow()
    if playMusic:
        menuMusic.fadeout(1000)
    fade.fade_black(6, "inGame")
else:
    gameState = "inGame"

currentlyPlaying = None

def startMusic(music):
    global currentlyPlaying
    global curChannel
    if curChannel.get_busy() and not music == currentlyPlaying:
        curChannel = music.play(-1)
        currentlyPlaying = music
    elif not curChannel.get_busy():
        curChannel = music.play(-1)
        currentlyPlaying = music

while run:
    clock.tick(60)
    if playMusic:
        startMusic(gameMusic)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if not save_file == None:
                player.save()
            run = False
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
            mouseX -= menuXOffset
            mouseX *= 480/winW
            mouseY *= 360/winH
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
    if player.falling and not fly:
        player.yVel -= level.gravity
    
    if keys[pygame.K_w] and player.touchingPlatform and player.jumping == 0 and not fly:
        player.jumping = 1
        player.yVel += 10
    if keys[pygame.K_f]:
        if not fly:
            player.yVel += 5
            fly = True
    elif keys[pygame.K_r]:
        fly = False
    if keys[pygame.K_t]:
        level = Level(level.src, player)
    if fly:
        if keys[pygame.K_w]:
            player.yVel = 5
        elif keys[pygame.K_s]:
            player.yVel = -5
        elif not  keys[pygame.K_g]:
            player.yVel *= 0.9
    if keys[pygame.K_x]:
        player.width = 30
        player.xOffset = 5
    else:
        player.xOffset = 0
        player.width = 40
    if keys[pygame.K_SPACE] and player.gunCooldown == 0:
        GDFSER_shoot.play()
        bulletspeed = 20
        level.projectiles.append(Bullet(player.gunX, -player.gunY, player.rightArm+(player.rightHand*player.facing), bulletspeed, player))
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
    pygame.display.set_caption("Skylands %d.%d.%d    FPS: %d X: %d Y: %d ~ %d %d"\
                               % (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH,
                                  FPS, player.x, player.y, camX+mouseX, camY-mouseY))

pygame.quit()
