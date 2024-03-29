from utils import *
from config import config
from timer import timers
from window import controller
from game import game_manager

class View:
    def __init__(self):
        self.background = None
        self.music_channel = None

    def set_background(self, texture):
        self.background = texture

    def start(self):
        pass

    def update(self):
        pass

    def render(self):
        win = controller.win

        if self.background != None:
            win.blit(self.background, (0, 0))

        return win

    def handle_keypress(self, key):
        pass

    def handle_key_release(self, key):
        pass

    def handle_click(self, mouseX, mouseY, button):
        pass

    def handle_music_end(self):
        pass


class IntroView(View):
    def __init__(self):
        super().__init__()

        self.set_background(controller.intro_credits)

    def handle_music_end(self):
        views.set_view("main_menu")

class MainMenuView(View):
    def __init__(self):
        super().__init__()

        self.page = "entry"
        self.credits_y = 0
        self.set_background(controller.menu_background)

    def start(self):
        controller.sound_ctrl.load_music("assets/music/Skylands Theme Loop.ogg")
        controller.sound_ctrl.play_music(loops=-1)

    def render(self):
        win = super().render()

        if self.page == "entry":
            win.blit(controller.play_text, (176, 306))
        elif self.page == "main":
            fonts = controller.fonts

            newGame = fonts["gemCount"].render("New Game", True, (170, 170, 190), (130, 132, 130))
            loadGame = fonts["gemCount"].render("Load Game", True, (170, 170, 190), (130, 132, 130))
            levelSelect = fonts["gemCount"].render("Level Select", True, (170, 170, 190), (130, 132, 130))
            settings = fonts["gemCount"].render("Settings", True, (170, 170, 190), (130, 132, 130))
            creditsText = fonts["buttonText"].render("Credits", True, (170, 170, 190), (130, 132, 130))
            returnText = fonts["buttonText"].render("Return", True, (170, 170, 190), (130, 132, 130))
            win.blit(newGame, (378, 16))
            win.blit(loadGame, (376, 54))
            win.blit(levelSelect, (373, 92))
            win.blit(settings, (387, 130))
            win.blit(creditsText, (23, 311))
            win.blit(returnText, (390, 311))
        elif self.page == "credits":
            win.fill((251, 251, 254))
            win.blit(controller.credits_slide, (0, min(self.credits_y, 0)))
            self.credits_y -= 1
            if self.credits_y < -1440 and not controller.fade.active:
                def after_fade():
                    self.set_background(controller.play_menu)
                    self.page = "main"
                controller.fade.fade_white(6, after_fade)


    def handle_keypress(self, key):
        if self.page == "entry":
            if key == pygame.K_SPACE:
                def after_fade():
                    self.set_background(controller.play_menu)
                    self.page = "main"
                
                controller.fade.fade_white(6, after_fade)
        elif self.page == "credits":
            if key == pygame.K_ESCAPE:
                def after_fade():
                    self.set_background(controller.play_menu)
                    self.page = "main"
                controller.fade.fade_white(6, after_fade)

    def handle_click(self, mouseX, mouseY, button):
        if self.page == "main":
            if button == 1:
                if 8<mouseY<42 and 362<mouseX<476:
                    #NEW GAME
                    controller.sound_ctrl.play_sound(controller.sounds["button"])
                    controller.sound_ctrl.stop_music(fadeout=1000)
                    game_manager.new_game()
                    def after_fade():
                        views.set_view("cutscene")
                    
                    controller.fade.fade_black(6, after_fade)
                    # level = Level("narbadhir1", win, win2, window, player, {}, sounds, vol)
                elif 46<mouseY<80 and 362<mouseX<476:
                    #LOAD
                    controller.sound_ctrl.play_sound(controller.sounds["button"])
                elif 122<mouseY<156 and 362<mouseX<476:
                    #SETTINGS
                    # button.play()
                    # controlsScreen("playMenu")
                    controller.sound_ctrl.play_sound(controller.sounds["button"])
                elif 304<mouseY<348 and 376<mouseX<468:
                    #RETURN
                    # button.play()
                    # fade.fade_white(6, "mainMenu")
                    controller.sound_ctrl.play_sound(controller.sounds["button"])
                    def after_fade():
                        self.set_background(controller.menu_background)
                        self.page = "entry"
                    
                    controller.fade.fade_white(6, after_fade)
                elif 304<mouseY<348 and 12<mouseX<104:
                    #CREDITS
                    self.credits_y = 40
                    controller.sound_ctrl.play_sound(controller.sounds["button"])
                    def after_fade():
                        self.set_background(None)
                        self.page = "credits"
                    
                    controller.fade.fade_white(8, after_fade)

class CutSceneView(View):
    def __init__(self):
        super().__init__()

        self.instructions = []
        self.textures = {}
        self.blits = []
        self.sounds = []

    def start(self):
        cutscene = game_manager.get_cutscene()
        if cutscene != None and config["enableCutscenes"]:
            f = open(resource_path("cutscenes/%s.txt" % (cutscene)))
            data = f.read().split("\n")
            f.close()
            self.instructions = [i.split(" ") for i in data]
            self.run_cutscene()
        else:
            self.next()

    def run_cutscene(self):
        while len(self.instructions) > 0:
            line = self.instructions[0]
            del self.instructions[0]
            if line[0] == "texture":
                self.textures[line[1]] = controller.load_texture("assets/%s" % (line[2]))
            elif line[0] == "music":
                print("assets/%s" % (' '.join(line[2:])))
                controller.sound_ctrl.load_music("assets/%s" % (' '.join(line[2:])))
                controller.sound_ctrl.play_music()
            elif line[0] == "sound":
                sound = controller.sound_ctrl.load_sound("assets/%s" % (' '.join(line[2:])))
                controller.sound_ctrl.play_sound(sound)
                self.sounds.append(sound)
            elif line[0] == "blit":
                self.blits.append((line[1], (int(line[2]), int(line[3]))))
            elif line[0] == "wait":
                timers.set_timeout(
                    lambda:
                        self.run_cutscene()
                    , int(line[1])
                )
                return

        self.next()

    def next(self):
        for sound in self.sounds:
            controller.sound_ctrl.unload_sound(sound)

        def after_fade():
            views.set_view("game")
        
        controller.fade.fade_black(6, after_fade)

    def render(self):
        win = super().render()

        win.fill((0, 0, 0))

        for data in self.blits:
            win.blit(self.textures[data[0]], data[1])

class GameView(View):
    def __init__(self):
        super().__init__()

    def start(self):
        pass

    def update(self):
        game_manager.update()

    def render(self):
        win = controller.win

        win.fill((240, 240, 255))
        game_manager.render()

    def handle_keypress(self, key):
        game_manager.handle_keypress(key)

    def handle_key_release(self, key):
        game_manager.handle_key_release(key)

    def handle_click(self, mouseX, mouseY, button):
        game_manager.handle_click(mouseX, mouseY, button)

    def handle_music_end(self):
        pass


class ViewController:
    def __init__(self):
        self.views = {
            "intro": IntroView(),
            "main_menu": MainMenuView(),
            "cutscene": CutSceneView(),
            "game": GameView(),
        }
        self.cur_view = None
    
    def set_view(self, view):
        self.cur_view = self.views[view]
        self.cur_view.start()

    def handle_event(self, event):
        if self.cur_view != None:
            if event.type == pygame.KEYDOWN:
                self.cur_view.handle_keypress(event.key)
            elif event.type == pygame.KEYUP:
                self.cur_view.handle_key_release(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ## Use controller.mouse_pos instead of event.pos to ensure correct scaling
                self.cur_view.handle_click(*controller.mouse_pos, event.button)
            elif event.type == MUSIC_END:
                self.cur_view.handle_music_end()

views = ViewController()