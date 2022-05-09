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

##def window_events(player, ): ADD OBJECT TO HANDLE MAIN CLASS VARIABLES
##    for event in pygame.event.get():
##        if event.type == pygame.QUIT:
##            if not save_file == None:
##                player.save()
##            run = False
##        if event.type == pygame.MOUSEMOTION:
##            mouseX, mouseY = event.pos
##            mouseX -= menuXOffset
##            mouseY -= menuYOffset
##            mouseX *= 480/winW
##            mouseY *= 360/winH
##        if event.type == pygame.MOUSEBUTTONDOWN:
##            if event.button == 1:
##                mouseX, mouseY = event.pos
##                mouseX -= menuXOffset
##                mouseY -= menuYOffset
##                mouseX *= 480/winW
##                mouseY *= 360/winH
##                if mouseY>318 and mouseX<42:
##                    if playMusic:
##                        curChannel.pause()
##                    pauseScreen("inGame")
##                    if playMusic:
##                        curChannel.unpause()
##        if event.type == pygame.VIDEORESIZE:
##            if event.w/480 > event.h/360:
##                winW, winH = int(480*(event.h/360)), event.h
##                menuXOffset = int(event.w/2) - int(480*(event.h/360)/2)
##                menuYOffset = 0
##            else:
##                winW, winH = event.w, int(360*(event.w/480))
##                menuXOffset = 0
##                menuYOffset = int(event.h/2) - int(360*(event.w/480)/2)
##            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
##            win2 = pygame.Surface((winW, winH))
##            #bg = pygame.transform.scale(sky, (event.w, event.h))
##            #menu = pygame.transform.scale(menuIsland, (480, 360))
##            pl = pygame.transform.scale(playText, (int(255*(event.h/720)), int(event.h/18)))
##            #menuXOffset = int(event.w/2) - int(960*(event.h/720)/2)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def play_cutscene(scene, win, win2, window, player, sounds, vol):
    sl = {
        'reboot':reboot,
        }
    sl[scene](win, win2, window, player, sounds, vol)

def reboot(win, win2, window, player, sounds, vol):
    bg = pygame.image.load(resource_path('assets\\reboot.png'))
    t = time()
    win.fill((0, 0, 0))
    pygame.transform.scale(win, (960, 720), win2)
    window.blit(win2, (0,0))
    pygame.display.update()
    while time()-t < 1:
        win.fill((0, 0, 0))
        pygame.transform.scale(win, (960, 720), win2)
        window.blit(win2, (0,0))
        pygame.display.update()
    win.blit(bg, (0, 0))
    pygame.transform.scale(win, (960, 720), win2)
    window.blit(win2, (0,0))
    pygame.display.update()
##    sounds['powerup'].play()
##    while time()-t < 4:
##        pygame.display.update()
    rbs = pygame.mixer.Sound(resource_path("assets\\sounds\\SCJingle.wav"))
    rbs.set_volume(1*vol)
    rbs.play()
    while time()-t < 5:
        win.blit(bg, (0, 0))
        pygame.transform.scale(win, (960, 720), win2)
        window.blit(win2, (0,0))
        pygame.display.update()
