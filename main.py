from utils import *
from window import WindowController, DISPLAY_WIDTH, DISPLAY_HEIGHT

## Handle command line args
## TODO

## Set Version Constants
VERSION_MAJOR = 0
VERSION_MINOR = 3
VERSION_PATCH = 1

controller = WindowController()
controller.set_version(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

## Create Views
from view import ViewController
views = ViewController(controller)

## Start intro music while loading to save time
intro_music_channel = controller.sound_ctrl.play_music(controller.menu_music_start)

from timer import TimerController
timers = TimerController()

timers.set_timeout(
    lambda:
        print("test")
    , 2000
)

timers.set_condition(
    lambda:
        views.set_view("main_menu")
    , lambda:
        intro_music_channel == None or not intro_music_channel.get_busy()
)

## TODO ALL OTHER LOADING HERE

controller.cl_intro()

## Set the intro view now that loading is complete
views.set_view("intro")

## globals
clock = pygame.time.Clock()
FPS = 60
held = {} # to detect which keys are being held down for an extended time
keys = pygame.key.get_pressed()
run = True # to control when the pygame main loop should quit

## pygame main loop
while run:
    clock.tick(FPS)
    timers.check_all()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ## initiate graceful exit (TODO)
            run = False
        elif event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
            mouseX -= controller.menu_offsets[0]
            mouseY -= controller.menu_offsets[1]
            mouseX *= DISPLAY_WIDTH / controller.win_size[0]
            mouseY *= DISPLAY_HEIGHT / controller.win_size[1]
            controller.mouse_pos = mouseX, mouseY
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            mouseX -= controller.menu_offsets[0]
            mouseY -= controller.menu_offsets[1]
            mouseX *= DISPLAY_WIDTH / controller.win_size[0]
            mouseY *= DISPLAY_HEIGHT / controller.win_size[1]
            controller.mouse_pos = mouseX, mouseY
            views.handle_event(event)
        elif event.type == pygame.VIDEORESIZE:
            if event.w / DISPLAY_WIDTH > event.h / DISPLAY_HEIGHT:
                controller.win_size = int(DISPLAY_WIDTH * (event.h / DISPLAY_HEIGHT)), event.h
                controller.menu_offsets = int(event.w / 2) - int(DISPLAY_WIDTH * (event.h / DISPLAY_HEIGHT) / 2), 0
            else:
                controller.win_size = event.w, int(DISPLAY_HEIGHT * (event.w / DISPLAY_WIDTH))
                controller.menu_offsets = 0, int(event.h / 2) - int(DISPLAY_HEIGHT * (event.w / DISPLAY_WIDTH) / 2)
            
            controller.win2 = pygame.Surface(controller.win_size)
        else:
            views.handle_event(event)

    held = keys
    keys = pygame.key.get_pressed()

    ## Render current view
    controller.render_view(views.cur_view)
