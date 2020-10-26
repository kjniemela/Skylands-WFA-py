try:
    import pygame
except ModuleNotFoundError:
    print("ModuleNotFoundError: Pygame module could not be found.")
    t=time()
    while time()-t<1:
        pass
    exit()
 
from entities import *

def loadLevelTextures(scale):
    global platformTextures
    global bullet
    platformTextures = {
        "ground1": pygame.image.load('assets/ground1.png')
        }
    bullet = pygame.image.load('assets/GDFSER-bullet.png')

def blitRotateCenter(surf, image, angle, pos, camPos):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect().center)

    surf.blit(rotated_image, (new_rect.topleft[0] + pos[0] - camPos[0], new_rect.topleft[1] + pos[1] + camPos[1]))

class Level:
    def __init__(self, src, scale, player):

        self.platforms = []
        self.projectiles = []
        self.entities = []

        self.player = player
        self.player.level = self

        self.entityTypes = {
            'shoaldier': Shoaldier
        }

        self.gravity = 0.5
        
        f = open("levels/"+src)
        data = f.read().split("\n")
        f.close()
        data = [i.split(" ") for i in data]
        for i in data:
            if i[1] == '1':
                self.platforms.append(Platform(i[0], int(i[2])*scale, int(i[3])*scale, int(i[4])*scale, int(i[5])*scale))
            elif i[1] == '2':
                self.entities.append(self.entityTypes[i[0]](self, int(i[2]*scale), int(i[3]*scale)))

    def draw(self, camX, camY, scale, win, mouseX, mouseY, winW, winH):
        for platform in self.platforms:
            win.blit(platform.texture, (platform.x-camX, -(platform.y-camY)))
        for projectile in self.projectiles:
            if projectile.tick() and not projectile.get_touching(self):
                blitRotateCenter(win, bullet, projectile.d, (projectile.x,-projectile.y), (camX,camY))
            else:
                del self.projectiles[self.projectiles.index(projectile)]
        for entity in self.entities:
            if entity.tick(scale):
                entity.draw(camX, camY, scale, win, mouseX, mouseY, winW, winH)
            else:
                del self.entities[self.entities.index(entity)]

class Platform:
    def __init__(self, texture, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.texture = platformTextures[texture]
