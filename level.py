try:
    import pygame
except ModuleNotFoundError:
    print("ModuleNotFoundError: Pygame module could not be found.")
    t=time()
    while time()-t<1:
        pass
    exit()


def loadLevelTextures(scale):
    global platformTextures
    global bullet
    platformTextures = {
        "ground1": pygame.transform.scale(pygame.image.load('assets/ground1.png'), (188*scale, 125*scale))
        }
    bullet = pygame.transform.scale(pygame.image.load('assets/GDFSER-bullet.png'), (int(26*scale/2), int(12*scale/2)))

def blitRotateCenter(surf, image, angle, pos, camPos):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect().center)

    surf.blit(rotated_image, (new_rect.topleft[0] + pos[0] - camPos[0], new_rect.topleft[1] + pos[1] + camPos[1]))

class Level:
    def __init__(self, src, scale):

        self.platforms = []
        self.projectiles = []
        
        f = open("levels/"+src)
        data = f.read().split("\n")
        f.close()
        data = [i.split(" ") for i in data]
        for i in data:
            if i[1] == '1':
                self.platforms.append(Platform(i[0], int(i[2])*scale, int(i[3])*scale, int(i[4])*scale, int(i[5])*scale))
    def draw(self, camX, camY, scale, win, mouseX, mouseY, winW, winH):
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
