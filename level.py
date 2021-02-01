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
        "tree": pygame.image.load(resource_path('assets/tree.png')),
##        "lab1Debug": pygame.image.load(resource_path('assets/lab1.png')).convert(),
##        "lab2Debug": pygame.image.load(resource_path('assets/lab2.png')).convert(),
##        "lab3Debug": pygame.image.load(resource_path('assets/lab3.png')).convert(),
##        "lab4Debug": pygame.image.load(resource_path('assets/lab4.png')).convert(),
        "lab1": pygame.image.load(resource_path('assets/lab1.png')),
        "lab2": pygame.image.load(resource_path('assets/lab2.png')),
        "lab3": pygame.image.load(resource_path('assets/lab3.png')),
        "lab4": pygame.image.load(resource_path('assets/lab4.png')),
        "lab_back1": pygame.image.load(resource_path('assets/lab_back1.png')),
        "lab_back2": pygame.image.load(resource_path('assets/lab_back2.png')),
        "lab_back3": pygame.image.load(resource_path('assets/lab_back3.png')),
        "lab_back4": pygame.image.load(resource_path('assets/lab_back4.png')),
        "door1": pygame.image.load(resource_path('assets/door1.png')),
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
    debugMode = False
    def __init__(self, src, player, music={}):

        self.platforms = []
        self.overlays = []
        self.background = []
        self.backdrop = []
        self.polyplats = []
        self.projectiles = []
        self.entities = []
        self.itemEntities = []

        self.controls = {}
        self.data = {}

        self.player = player
        self.player.level = self
        self.src = src

        self.tracks = {}

        for track in music:
            self.tracks[track] = (pygame.mixer.Sound(resource_path(music[track])))

        self.entityTypes = {
            "shoaldier": Shoaldier,
            "doorController": DoorController
        }

        self.achievement_handler = AchievementRenderer()

        self.gravity = 0.5
        
        f = open(resource_path("levels/"+src))
        data = f.read().split("\n")
        f.close()
        data = [i.split(" ") for i in data]
        for i in data:
            if i[0] == 'plat':
                self.platforms.append(Platform(i[1], int(i[2]), int(i[3]), int(i[4]), int(i[5]), int(i[6]), i[1] != "none"))
                if len(i) > 7:
                    self.controls[i[7]] = self.platforms[-1]
            elif i[0] == 'platc':
                self.platforms.append(Platform(i[1], int(i[2])+(int(i[4])//2), int(i[3])-(int(i[5])//2), int(i[4]), int(i[5]), int(i[6]), i[1] != "none"))
                if len(i) > 7:
                    self.controls[i[7]] = self.platforms[-1]
            elif i[0] == 'overlay':
                self.overlays.append(Platform(i[1], int(i[2]), int(i[3]), int(i[4]), int(i[5]), int(i[6])))
            elif i[0] == 'backg':
                self.background.append(Platform(i[1], int(i[2]), int(i[3]), int(i[4]), int(i[5]), int(i[6])))
            elif i[0] == 'backdr':
                self.backdrop.append(((int(i[1]), int(i[2]), int(i[3])), (int(i[4]), int(i[5]), int(i[6]), int(i[7]))))
            elif i[0] == 'poly':##Never use polyplats. Use a combination of platforms instead
                self.polyplats.append(PolyPlat((int(i[1]), int(i[2]), int(i[3])), i[4:]))
            elif i[0] == 'entity':
                self.entities.append(self.entityTypes[i[1]](self, int(i[2]), int(i[3])))
                if len(i) > 4:
                    self.controls[i[4]] = self.entities[-1]
            elif i[0] == 'spawn':
                self.player.set_spawn(int(i[1]), int(i[2]))
            elif i[0] == 'script':
                from scripts import get_script
                script = get_script(i[1])
                if not script == None:
                    self.tick = script
            elif i[0] == 'music':
                self.tracks[i[1]] = (pygame.mixer.Sound(resource_path(' '.join(i[2:]))))
        #self.generate(50)\

        try:
            self.curTrack = list(self.tracks.keys())[0]
        except IndexError:
            self.curTrack = None
    def tick(self, level):
        pass
    def generate(self, times):
        plat_x = -200
        plat_y = 0
        d = 0
        self.platforms = [Platform("ground1", plat_x-94, plat_y-63, 188, 125, 0)]
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
        self.tick(self)
        for backdr in self.backdrop:
            if distance(self.player.x, self.player.y, backdr[1][0], backdr[1][1]) < max(backdr[1][2]/2, backdr[1][3]/2)+240:
                pygame.draw.rect(win, backdr[0], (backdr[1][0]-camX-backdr[1][2]/2, -(backdr[1][1]-camY)-backdr[1][3]/2, *backdr[1][2:]))
        for backg in self.background:
            if distance(self.player.x, self.player.y, backg.x, backg.y) < max(backg.w/2, backg.h/2)+400:
                if backg.d == 0:
                    win.blit(backg.texture, (backg.x-(backg.w/2)-camX, -(backg.y+(backg.h/2)-camY)))
                else:
                    blitRotateCenter(win, backg.texture, backg.d, (backg.x-(backg.w/2),-(backg.y+(backg.h/2))), (camX,camY))
        for platform in self.platforms:
##            if distance(self.player.x, self.player.y, platform.x, platform.y) < max(platform.w/2, platform.h/2)+120:
##                verts = platform.get_verts(camX, camY, 1.001)
##                v = []
##                for vert in verts:
##                    if not platform.collides_with_line(self.player.x, self.player.y, vert[0], vert[1]):
##                        point = screen_coords(vert, camX, camY)
##                        plcoords = screen_coords((self.player.x, self.player.y), camX, camY)
##                        if point[1] < plcoords[1]:
##                            l = extend_line_up(*point, *plcoords, 0)
##                            v.append((l[0], l[1]))
##                            v.append(point)
##                        else:
##                            l = extend_line_down(*point, *plcoords, 360)
##                            v.append((l[0], l[1]))
##                            v.append(point)
##                #print(v)
##                if len(v) == 4:
##                    pygame.draw.polygon(win, 0, [v[0], v[1], v[3], v[2]])
##                elif len(v) == 6:
##                    pygame.draw.polygon(win, 0, [v[0], v[1], v[5], v[3], v[2], v[4]])
            if platform.visible:
                if distance(self.player.x, self.player.y, platform.x, platform.y) < max(platform.w/2, platform.h/2)+240:
                    if platform.d == 0:
                        win.blit(platform.texture, (platform.x-(platform.w/2)-camX, -(platform.y+(platform.h/2)-camY)))
                    else:
                        blitRotateCenter(win, platform.texture, platform.d, (platform.x-(platform.w/2),-(platform.y+(platform.h/2))), (camX,camY))
            elif self.debugMode:
                if platform.d == 0:
                        pygame.draw.rect(win, (0, 0, 0),
                                     (platform.x-camX-platform.w/2,
                                      -(platform.y-camY)-platform.h/2,
                                      platform.w, platform.h))
                else:     
                    x1 = platform.x-((platform.w/2)*Cos(-platform.d))+((platform.h/2)*Sin(-platform.d))
                    y1 = platform.y+((platform.h/2)*Cos(-platform.d))+((platform.w/2)*Sin(-platform.d))
                    x2 = platform.x+((platform.w/2)*Cos(-platform.d))+((platform.h/2)*Sin(-platform.d))
                    y2 = platform.y+((platform.h/2)*Cos(-platform.d))-((platform.w/2)*Sin(-platform.d))
                    
                    x3 = platform.x-((platform.w/2)*Cos(-platform.d))-((platform.h/2)*Sin(-platform.d))
                    y3 = platform.y-((platform.h/2)*Cos(-platform.d))+((platform.w/2)*Sin(-platform.d))
                    x4 = platform.x+((platform.w/2)*Cos(-platform.d))-((platform.h/2)*Sin(-platform.d))
                    y4 = platform.y-((platform.h/2)*Cos(-platform.d))-((platform.w/2)*Sin(-platform.d))
                    pygame.draw.polygon(win, (0, 0, 0), [
                        (x1-camX, -(y1-camY)),
                        (x2-camX, -(y2-camY)),
                        (x4-camX, -(y4-camY)),
                        (x3-camX, -(y3-camY)),
                        ])
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
    def draw_overlays(self, camX, camY, win, mouseX, mouseY, winW, winH):
        if self.debugMode:
            for overlay in self.overlays:
                if distance(self.player.x, self.player.y, overlay.x, overlay.y) < max(overlay.w/2, overlay.h/2)+400:
                    if overlay.d == 0:
                        overlay.debugTexture.set_alpha(100)
                        win.blit(overlay.debugTexture, (overlay.x-(overlay.w/2)-camX, -(overlay.y+(overlay.h/2)-camY)))
                    else:
                        blitRotateCenter(win, overlay.debugTexture, overlay.d, (overlay.x-(overlay.w/2),-(overlay.y+(overlay.h/2))), (camX,camY))
        else:
            for overlay in self.overlays:
                if distance(self.player.x, self.player.y, overlay.x, overlay.y) < max(overlay.w/2, overlay.h/2)+400:
                    if overlay.d == 0:
                        win.blit(overlay.texture, (overlay.x-(overlay.w/2)-camX, -(overlay.y+(overlay.h/2)-camY)))
                    else:
                        blitRotateCenter(win, overlay.texture, overlay.d, (overlay.x-(overlay.w/2),-(overlay.y+(overlay.h/2))), (camX,camY))

class PolyPlat:##DEFUNCT
    def __init__(self, color, points):
        self.color = color
        self.points = []
        for i in range(0, len(points), 2):
            self.points.append((int(points[i]), int(points[i+1])))

cursor = pygame.image.load(resource_path('assets/cursor.png'))
            
class Platform:
    def __init__(self, texture, x, y, w, h, d, visible=True):
        self.x, self.y, self.w, self.h, self.d, self.visible = x, y, w, h, d, visible
        if visible == True:
            self.texture = platformTextures[texture]
            try:
                self.debugTexture = platformTextures[texture+"Debug"]
            except KeyError:
               self.debugTexture = platformTextures[texture].convert()
    def get_verts(self, camX, camY, b=1):
        x1 = self.x-((self.w/2)*Cos(-self.d)*b)+((self.h/2)*Sin(-self.d)*b)
        y1 = self.y+((self.h/2)*Cos(-self.d)*b)+((self.w/2)*Sin(-self.d)*b)
        x2 = self.x+((self.w/2)*Cos(-self.d)*b)+((self.h/2)*Sin(-self.d)*b)
        y2 = self.y+((self.h/2)*Cos(-self.d)*b)-((self.w/2)*Sin(-self.d)*b)
        
        x3 = self.x-((self.w/2)*Cos(-self.d)*b)-((self.h/2)*Sin(-self.d))
        y3 = self.y-((self.h/2)*Cos(-self.d)*b)+((self.w/2)*Sin(-self.d))
        x4 = self.x+((self.w/2)*Cos(-self.d)*b)-((self.h/2)*Sin(-self.d))
        y4 = self.y-((self.h/2)*Cos(-self.d)*b)-((self.w/2)*Sin(-self.d))

        return [
            (x1, y1),
            (x2, y2),
            (x3, y3),
            (x4, y4)
            ]

##        return [
##            (x1-camX, -(y1-camY)),
##            (x2-camX, -(y2-camY)),
##            (x3-camX, -(y3-camY)),
##            (x4-camX, -(y4-camY))
##            ]
        
    def collides_with_line(self, px1, py1, px2, py2):
        x1 = self.x-((self.w/2)*Cos(-self.d))+((self.h/2)*Sin(-self.d))
        y1 = self.y+((self.h/2)*Cos(-self.d))+((self.w/2)*Sin(-self.d))
        x2 = self.x+((self.w/2)*Cos(-self.d))+((self.h/2)*Sin(-self.d))
        y2 = self.y+((self.h/2)*Cos(-self.d))-((self.w/2)*Sin(-self.d))
        
        x3 = self.x-((self.w/2)*Cos(-self.d))-((self.h/2)*Sin(-self.d))
        y3 = self.y-((self.h/2)*Cos(-self.d))+((self.w/2)*Sin(-self.d))
        x4 = self.x+((self.w/2)*Cos(-self.d))-((self.h/2)*Sin(-self.d))
        y4 = self.y-((self.h/2)*Cos(-self.d))-((self.w/2)*Sin(-self.d))

##        blitRotateCenter(win, cursor, 0, (x1-8, -y1-8), (camX,camY))
##        blitRotateCenter(win, cursor, 0, (x2-8, -y2-8), (camX,camY))
##        blitRotateCenter(win, cursor, 0, (x3-8, -y3-8), (camX,camY))
##        blitRotateCenter(win, cursor, 0, (x4-8, -y4-8), (camX,camY))
##        pygame.draw.aaline(win, (111, 255, 239, 0.5), (x1-camX, -(y1-camY)), (x2-camX, -(y2-camY)))
##        pygame.draw.aaline(win, (111, 255, 239, 0.5), (x2-camX, -(y2-camY)), (x4-camX, -(y4-camY)))
##        pygame.draw.aaline(win, (111, 255, 239, 0.5), (x3-camX, -(y3-camY)), (x4-camX, -(y4-camY)))
##        pygame.draw.aaline(win, (111, 255, 239, 0.5), (x3-camX, -(y3-camY)), (x1-camX, -(y1-camY)))
        #self.d = (self.d+1)%360

        if line_collision((px1, py1, px2, py2), (x1, y1, x2, y2))[0]:
            #print(line_collision((px1, py1, px2, py2), (x1, y1, x2, y2)))
            #pygame.draw.aaline(win, (255, 0, 0, 0.5), (px1-camX, -(py1-camY)), (px2-camX, -(py2-camY)))
            return True
        elif line_collision((px1, py1, px2, py2), (x3, y3, x4, y4))[0]:
            #print(line_collision((px1, py1, px2, py2), (x3, y3, x4, y4)))
            #pygame.draw.aaline(win, (255, 0, 0, 0.5), (px1-camX, -(py1-camY)), (px2-camX, -(py2-camY)))
            return True
        elif line_collision((px1, py1, px2, py2), (x2, y2, x4, y4))[0]:
            #print(line_collision((px1, py1, px2, py2), (x2, y2, x4, y4)))
            #pygame.draw.aaline(win, (255, 0, 0, 0.5), (px1-camX, -(py1-camY)), (px2-camX, -(py2-camY)))
            return True
        elif line_collision((px1, py1, px2, py2), (x3, y3, x1, y1))[0]:
            #print(line_collision((px1, py1, px2, py2), (x3, y3, x1, y1)))
            #pygame.draw.aaline(win, (255, 0, 0, 0.5), (px1-camX, -(py1-camY)), (px2-camX, -(py2-camY)))
            return True
        else:
            #pygame.draw.aaline(win, (0, 255, 0, 0.5), (px1-camX, -(py1-camY)), (px2-camX, -(py2-camY)))
            return False
