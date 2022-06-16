from utils import *
from window import WindowController

class View:
    def __init__(self, controller: WindowController):
        self.controller = controller
        self.background = None

    def set_background(self, texture):
        self.background = texture

    def start(self):
        pass

    def render(self):
        win = self.controller.win

        win.blit(self.background, (0, 0))

        return win

class IntroView(View):
    def __init__(self, controller: WindowController):
        super().__init__(controller)

        self.set_background(controller.intro_credits)

class MainMenuView(View):
    def __init__(self, controller: WindowController):
        super().__init__(controller)

        self.set_background(controller.sky)

    def start(self):
        self.controller.sound_ctrl.play_music(self.controller.menu_music)

    def render(self):
        win = super().render()

        win.blit(self.controller.menu_island, (0, 0))
        win.blit(self.controller.play_text, (176, 306))


class ViewController:
    def __init__(self, controller: WindowController):
        self.controller = controller
        self.views = {
            "intro": IntroView(controller),
            "main_menu": MainMenuView(controller),
        }
        self.cur_view = None
    
    def set_view(self, view):
        self.cur_view = self.views[view]
        self.cur_view.start()