from utils import *
from config import config

## Set Version Constants
VERSION_MAJOR = 0
VERSION_MINOR = 3
VERSION_PATCH = 1

## Handle command line args
i = 0
while i < len(sys.argv):
    try:
        flag = sys.argv[i]
        if flag == "-h":
            print("Skylands %i.%i.%i" % (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH))
            print("usage: python main.py")
            print("Options and arguments:")
            print("  -h              print this message and exit")
            print("  -s [save_file]  load game state from the provided file")
            print("  -m [Y/n]        override the config.enableMusic option")
            print("  -a [Y/n]        override the config.enableSound option")
            print("  -d              launch Skylands in debug mode")
            print("  -D              debug mode + disable sounds / transitions")

            sys.exit()
        elif flag == "-s":
            i += 1
            arg = sys.argv[i]
            if input("Loading games from file is not fully supported yet! Continue anyway? [Y/n] ").lower() != "y":
                sys.exit()
        elif flag == "-m":
            i += 1
            arg = sys.argv[i]
            config["enableMusic"] = True if arg.lower() == "y" else False
        elif flag == "-a":
            i += 1
            arg = sys.argv[i]
            config["enableSound"] = True if arg.lower() == "y" else False
        elif flag == "-d":
            config["debug"] = True
        elif flag == "-D":
            config["debug"] = True
            config["enableMusic"] = False
            config["enableSound"] = False
            config["enableCutscenes"] = False
            config["enableFade"] = False

        i += 1
    except IndexError:
        print("Malformed or missing argument for flag \"%s\". Exiting." % (flag))
        sys.exit()

from window import controller, DISPLAY_WIDTH, DISPLAY_HEIGHT
controller.set_version(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

from timer import timers

## Create Views
from view import views

## Start intro music while loading to save time
controller.sound_ctrl.load_music("assets/music/Skylands Theme Start.ogg")
controller.sound_ctrl.play_music()

# timers.set_condition(
#     lambda:
#         views.set_view("main_menu")
#     ,
#     lambda:
#         intro_music_channel == None or not intro_music_channel.get_busy()
# )

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
    views.cur_view.update()
    controller.render_view(views.cur_view)

    ## If in debug mode, show debug data
    if config["debug"]:
        pygame.display.set_caption(
            "Skylands %d.%d.%d - Mouse Pos: %d / %d"
            % (
                VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH,
                controller.mouse_pos[0], controller.mouse_pos[1]
            )
        )
