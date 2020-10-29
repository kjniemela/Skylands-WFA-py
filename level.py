from random import randint
try:
    import pygame
except ModuleNotFoundError:
    print("ModuleNotFoundError: Pygame module could not be found.")
    t=time()
    while time()-t<1:
        pass
    exit()
 
from entities import *

def loadLevelTextures():
    global platformTextures
    global bullet
    platformTextures = {
        "ground1": pygame.image.load(resource_path('assets/ground1.png')),
        "grass1": pygame.image.load(resource_path('assets/grass1.png')),
        }
    bullet = pygame.image.load(resource_path('assets/GDFSER-bullet.png'))

def blitRotateCenter(surf, image, angle, pos, camPos):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect().center)

    surf.blit(rotated_image, (new_rect.topleft[0] + pos[0] - camPos[0], new_rect.topleft[1] + pos[1] + camPos[1]))

class AchievementRenderer:
    def __init__(self):
        self.achievements_got = { #add loading achievements from save files?
            "ANewStart": False,
            "BabySteps": False,
            "ChickeningOut": False,
            "Dropout": False,
            "HowBizarre": False,
            "Scrooge": False,
            "StillAlive": False,
            "StrangePeople": False
            }
        self.achievement_title = {
            "ANewStart": "A New Start",
            "BabySteps": "Baby Steps",
            "ChickeningOut": "Chickening Out",
            "Dropout": "Drop Out",
            "HowBizarre": "How Bizarre",
            "Scrooge": "Scrooge",
            "StillAlive": "Still Alive",
            "StrangePeople": "Strange People"
            }
        self.achievement_sub = {
            "ANewStart": False,
            "BabySteps": False,
            "ChickeningOut": False,
            "Dropout": False,
            "HowBizarre": False,
            "Scrooge": False,
            "StillAlive": False,
            "StrangePeople": False
            }

        self.on_display = ""
        self.is_displaying = False
        self.displayTime = 0
        self.queue = []

        self.text_bar = pygame.image.load(resource_path('assets/achievements/textBar.png'))

        self.achievement_assets = {}

        for i in self.achievements_got:
            self.achievement_assets[i] = pygame.image.load(resource_path('assets/achievements/%s.png' % (i)))
    def trigger(self, name):
        if not self.achievements_got[name]:
            self.achievements_got[name] = True
            if not self.is_displaying:
                self.is_displaying = True
                self.on_display = name
            else:
                self.queue.append(name)
    def message(self, win, fonts):
        pass
    def draw(self, win, level, fonts):
        if not self.achievements_got["ANewStart"]:
            self.trigger("ANewStart")
        if not self.achievements_got["Dropout"]:
            if level.player.y < -1000:
                self.trigger("Dropout")
        if not self.is_displaying:
            if len(self.queue) > 0:
                self.achievements_got[self.queue[0]] = True
                self.on_display = self.queue[0]
                self.is_displaying = True
                del self.queue[0]
        else:
            text = fonts["achievementTitle"].render(self.achievement_title[self.on_display], True, (170, 170, 190))
            titleXOffset = (100-text.get_rect().w)//2
            titleYOffset = 14
            if self.displayTime < 30:
                self.displayTime += 1
                win.blit(self.achievement_assets[self.on_display], (-60+(self.displayTime)*2, 0))
                win.blit(self.text_bar, (50, (-60+(self.displayTime)*2)))
                win.blit(text, (50+titleXOffset, (titleYOffset-60+(self.displayTime)*2)))
            elif self.displayTime < 240:
                self.displayTime += 1
                win.blit(self.achievement_assets[self.on_display], (0, 0))
                win.blit(self.text_bar, (50, 0))
                win.blit(text, (50+titleXOffset, titleYOffset))
            elif self.displayTime < 270:
                self.displayTime += 1
                win.blit(self.achievement_assets[self.on_display], (-(self.displayTime-240)*2, 0))
                win.blit(self.text_bar, (50, (-(self.displayTime-240)*2)))
                win.blit(text, (50+titleXOffset, (titleYOffset-(self.displayTime-240)*2)))
            else:
                self.on_display = ""
                self.is_displaying = False
                self.displayTime = 0

class Level:
    def __init__(self, src, player):

        self.platforms = []
        self.polyplats = []
        self.projectiles = []
        self.entities = []
        self.itemEntities = []

        self.player = player
        self.player.level = self

        self.entityTypes = {
            'shoaldier': Shoaldier
        }

        self.achievement_handler = AchievementRenderer()

        self.gravity = 0.5
        
        f = open(resource_path("levels/"+src))
        data = f.read().split("\n")
        f.close()
        data = [i.split(" ") for i in data]
        for i in data:
            if i[0] == 'plat':
                self.platforms.append(Platform(i[1], int(i[2]), int(i[3]), int(i[4]), int(i[5]), int(i[6])))
            elif i[0] == 'poly':
                self.polyplats.append(PolyPlat((int(i[1]), int(i[2]), int(i[3])), i[4:]))
            elif i[0] == 'entity':
                self.entities.append(self.entityTypes[i[1]](self, int(i[2]), int(i[3])))

        self.generate(50)
    def generate(self, times):
        plat_x = -200
        plat_y = 0
        d = 0
        self.platforms = []
        self.polyplats = [PolyPlat((79, 127, 0), [plat_x, -250])]
        self.entities = []
        for i in range(times):
            if randint(0, 5) == 0:
                self.entities.append(self.entityTypes["shoaldier"](self, plat_x+94, plat_y+200))
            self.polyplats[0].points.append((plat_x, plat_y))
            plat_x += (188*Cos(d))
            plat_y += (188*Sin(d))
            d = max(-50, min(50, d + randint(-10, 10)))
            if plat_y < -200:
                d = randint(0, 50)
        self.polyplats[0].points.append((plat_x, -250))
    def draw(self, camX, camY, win, mouseX, mouseY, winW, winH):
        for platform in self.platforms:
            if platform.d == 0:
                win.blit(platform.texture, (platform.x-(platform.w/2)-camX, -(platform.y+(platform.h/2)-camY)))
            else:
                blitRotateCenter(win, platform.texture, platform.d, (platform.x-(platform.w/2),-(platform.y+(platform.h/2))), (camX,camY))
        for polyplat in self.polyplats:
            pygame.draw.polygon(win, polyplat.color, [(x-camX, -(y-camY)) for x, y in polyplat.points])
        for entity in self.entities:
            if entity.tick():
                entity.draw(camX, camY, win, mouseX, mouseY, winW, winH)
            else:
                del self.entities[self.entities.index(entity)]
        for projectile in self.projectiles:
            if projectile.tick() and not projectile.get_touching(self):
                pygame.draw.aaline(win, (111, 255, 239, 0.5), ((projectile.x-camX),-(projectile.y-camY)), ((projectile.x-camX-projectile.xVel),-(projectile.y-camY-projectile.yVel)))
                blitRotateCenter(win, bullet, projectile.d, (projectile.x-6,-projectile.y-3), (camX,camY))
            else:
                del self.projectiles[self.projectiles.index(projectile)]

class PolyPlat:
    def __init__(self, color, points):
        self.color = color
        self.points = []
        for i in range(0, len(points), 2):
            self.points.append((int(points[i]), int(points[i+1])))
class Platform:
    def __init__(self, texture, x, y, w, h, d):
        self.x, self.y, self.w, self.h, self.d = x, y, w, h, d
        self.texture = platformTextures[texture]
