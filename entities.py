try:
    import pygame
except ModuleNotFoundError:
    print("ModuleNotFoundError: Pygame module could not be found.")
    t=time()
    while time()-t<1:
        pass
    exit()

shoaldierRight = {}
shoaldierLeft = {}

def loadEntityTextures(scale):
    global shoaldierRight
    global shoaldierLeft

    shoaldier = [
        ('arm_far', 22, 10),
        ('arm_near', 22, 12),
        ('foot_far', 22, 12),
        ('foot_near', 22, 12),
        ('hand_far', 22, 12),
        ('hand_near', 22, 12),
        ('hat', 22, 12),
        ('head', 22, 12),
        ('jaw', 22, 12),
        ('leg_far', 22, 12),
        ('leg_near', 22, 12),
        ('torso', 22, 12)
    ]
    for i in shoaldier:
        shoaldierRight[i[0]] = pygame.transform.scale(pygame.image.load('assets/shoaldier/%s.png'%(i[0])), (i[1]*scale, i[2]*scale))
        shoaldierLeft[i[0]] = pygame.transform.flip(shoaldierRight[i[0]], False, True)

    #print(shoaldierRight, shoaldierLeft)