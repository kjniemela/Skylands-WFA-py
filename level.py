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
        "ground1": pygame.image.load('assets/ground1.png')
        }
    bullet = pygame.image.load('assets/GDFSER-bullet.png')

def blitRotateCenter(surf, image, angle, pos, camPos):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect().center)

    surf.blit(rotated_image, (new_rect.topleft[0] + pos[0] - camPos[0], new_rect.topleft[1] + pos[1] + camPos[1]))

class Level:
    def __init__(self, src, player):

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
                self.platforms.append(Platform(i[0], int(i[2]), int(i[3]), int(i[4]), int(i[5])))
            elif i[1] == '2':
                self.entities.append(self.entityTypes[i[0]](self, int(i[2]), int(i[3])))

    def draw(self, camX, camY, win, mouseX, mouseY, winW, winH):
        for platform in self.platforms:
            win.blit(platform.texture, (platform.x-camX, -(platform.y-camY)))
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

class Platform:
    def __init__(self, texture, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.texture = platformTextures[texture]
