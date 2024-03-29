from utils import *
from config import config

## Load version and set constants
f = open(resource_path("version.txt"))
version_string = f.read()
f.close()
(
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_PATCH
) = version_string.split(".")

## Handle command line args
i = 0
while i < len(sys.argv):
    try:
        flag = sys.argv[i]
        if flag == "-h":
            print("Skylands %s.%s.%s" % (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH))
            print("usage: python main.py [options]")
            print("Options and arguments:")
            print("  -h              print this message and exit")
            print("  -s [save_file]  load game state from the provided file")
            print("  -m [Y/n]        override the config.enableMusic option")
            print("  -a [Y/n]        override the config.enableSound option")
            print("  -d              launch Skylands in debug mode")
            print("  -v              launch Skylands in verbose debug mode")
            print("  -D              debug mode + disable sounds / transitions")
            print("  -i [script]     load script in verbose debug mode and exit")
            print("  -L [level]      load level directly and skip the menu")

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
        elif flag == "-i":
            i += 1
            arg = sys.argv[i]
            config["debug"] = True
            config["verbose"] = True
            from world.level import Level
            from player import Player
            from game import game_manager
            level = Level(game_manager, arg, {})
            player = Player(level, Vec(0, 0))
            level.set_player(player)
            level.start()
            sys.exit()
        elif flag == "-L":
            i += 1
            arg = sys.argv[i]
            config["displayMenu"] = False
            from game import game_manager
            game_manager.set_level(arg)
            from view import views
            views.set_view('game')

        elif flag == "-v":
            config["debug"] = True
            config["verbose"] = True

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
if config["displayMenu"]:
    controller.sound_ctrl.load_music("assets/music/Skylands Theme Start.ogg")
    controller.sound_ctrl.play_music()

if config["debug"]:
    from game import game_manager

## TODO ALL OTHER LOADING HERE

controller.cl_intro()

## Set the intro view now that loading is complete
if config["displayMenu"]:
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
            controller.mouse_pos = Vec(mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            mouseX -= controller.menu_offsets[0]
            mouseY -= controller.menu_offsets[1]
            mouseX *= DISPLAY_WIDTH / controller.win_size[0]
            mouseY *= DISPLAY_HEIGHT / controller.win_size[1]
            controller.mouse_pos = Vec(mouseX, mouseY)
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
            "Skylands %s.%s.%s - Mouse Pos: %d / %d - World Mouse Pos: %d / %d"
            % (
                VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH,
                controller.mouse_pos[0], controller.mouse_pos[1],
                game_manager.camera_pos.x + controller.mouse_pos.x, game_manager.camera_pos.y - controller.mouse_pos.y
            )
        )
