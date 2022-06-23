from utils import *
from vec import Vec
from window import controller
from world.level import Level
from player import Player

class AchievementRenderer:
    def __init__(self):
        self.achievements_got = { #add loading achievements from save files?
            "ANewStart": False,
            "BabySteps": False,
            "ChickeningOut": False,
            "Dropout": False,
            "HowBizarre": False,
            "Scrooge": False,
            "StillAlive": False,
            "StrangePeople": False
        }
        self.achievement_title = {
            "ANewStart": "A New Start",
            "BabySteps": "Baby Steps",
            "ChickeningOut": "Chickening Out",
            "Dropout": "Drop Out",
            "HowBizarre": "How Bizarre",
            "Scrooge": "Scrooge",
            "StillAlive": "Still Alive",
            "StrangePeople": "Strange People"
        }

        self.on_display = ""
        self.is_displaying = False
        self.displayTime = 0
        self.queue = []

        self.text_bar = pygame.image.load(resource_path('assets/achievements/textBar.png'))

        self.achievement_assets = {}

        for i in self.achievements_got:
            self.achievement_assets[i] = pygame.image.load(resource_path('assets/achievements/%s.png' % (i)))
    def trigger(self, name):
        if not self.achievements_got[name]:
            self.achievements_got[name] = True
            if not self.is_displaying:
                self.is_displaying = True
                self.on_display = name
            else:
                self.queue.append(name)
    def message(self, win, fonts):
        pass
    def draw(self, win, level, fonts):
        if not self.achievements_got["ANewStart"]:
            self.trigger("ANewStart")
        if not self.achievements_got["Dropout"]:
            if level.player.pos.y < -1000:
                self.trigger("Dropout")
        if not self.is_displaying:
            if len(self.queue) > 0:
                self.achievements_got[self.queue[0]] = True
                self.on_display = self.queue[0]
                self.is_displaying = True
                del self.queue[0]
        else:
            text = fonts["achievementTitle"].render(self.achievement_title[self.on_display], True, (170, 170, 190))
            titleXOffset = (100-text.get_rect().w)//2
            titleYOffset = 14
            if self.displayTime < 30:
                self.displayTime += 1
                win.blit(self.achievement_assets[self.on_display], (-60+(self.displayTime)*2, 0))
                win.blit(self.text_bar, (50, (-60+(self.displayTime)*2)))
                win.blit(text, (50+titleXOffset, (titleYOffset-60+(self.displayTime)*2)))
            elif self.displayTime < 240:
                self.displayTime += 1
                win.blit(self.achievement_assets[self.on_display], (0, 0))
                win.blit(self.text_bar, (50, 0))
                win.blit(text, (50+titleXOffset, titleYOffset))
            elif self.displayTime < 270:
                self.displayTime += 1
                win.blit(self.achievement_assets[self.on_display], (-(self.displayTime-240)*2, 0))
                win.blit(self.text_bar, (50, (-(self.displayTime-240)*2)))
                win.blit(text, (50+titleXOffset, (titleYOffset-(self.displayTime-240)*2)))
            else:
                self.on_display = ""
                self.is_displaying = False
                self.displayTime = 0

class GameManager:
    def __init__(self):
        self.level = None
        self.achievement_handler = AchievementRenderer()

        self.next_entity_id = 0

        self.camera_pos = Vec(-240, 0)
        self.player = None
        self.previous_player_pos = (0, 0)

        self.controls = {
            "left": False,
            "jump": False,
            "right": False,
            "sneak": False,
            "shoot": False,
            "reload": False,
            "pause": False,
            "fly": False,
            "reset": False,
        }

        self.controls_keys_map = {
            "left": pygame.K_a,
            "jump": pygame.K_w,
            "right": pygame.K_d,
            "sneak": pygame.K_s,
            "shoot": pygame.K_SPACE,
            "reload": pygame.K_r,
            "pause": pygame.K_ESCAPE,
            "fly": pygame.K_f,
            "reset": pygame.K_t,
        }
        self.keys_controls_map = {self.controls_keys_map[key]: key for key in self.controls_keys_map}

    def get_next_entity_id(self):
        self.next_entity_id += 1
        return self.next_entity_id - 1

    def get_cutscene(self):
        if self.level != None:
            if self.level.cutscene != None:
                return self.level.cutscene
        
        return None

    def set_level(self, level_name):
        self.level = Level(self, level_name, controller.sounds)
        self.player = Player(self.level, Vec(0, 0))
        self.level.set_player(self.player)
        self.level.start()

    def new_game(self):
        self.level = 1
        # self.set_level("narbadhir1")
        self.set_level("test")

    def render_hud(self):
        win = controller.win
        player_textures = controller.player_textures

        win.blit(player_textures["health"], (435 - (142 * (self.player.hp / self.player.max_hp)), 28))
        win.blit(player_textures["power"], (443 - (110 * (self.player.power / self.player.max_power)), 40))     
        win.blit(player_textures["gem_icon"][int((time() * 16) % 9)], (10, 10))
        win.blit(controller.fonts["gemCount"].render('x%d' % (self.player.gems), True, (91, 183, 0)) , (50, 22))
        if self.player.quest != "":
            win.blit(player_textures["directive"], (55,305))
            win.blit(player_textures["dir_letters"][self.player.quest[0]], (200,315))
            win.blit(player_textures["dir_numbers"][self.player.quest[1]], (220,315))
            win.blit(player_textures["dir_numbers"][self.player.quest[2]], (235,315))
            win.blit(player_textures["dir_numbers"][self.player.quest[3]], (250,315))

    def handle_keypress(self, key):
        if key in self.keys_controls_map:
            control = self.keys_controls_map[key]
            self.controls[control] = True

    def handle_key_release(self, key):
        if key in self.keys_controls_map:
            control = self.keys_controls_map[key]
            self.controls[control] = False


    def handle_click(self, mouseX, mouseY, button):
        pass    

    def update(self):
        self.level.update()
        
        self.camera_pos.x += (((self.player.pos.x + 5) - (480 / 2)) - self.camera_pos.x) * 0.2
        self.camera_pos.y += (((self.player.pos.y + 20) + (360 / 2)) - self.camera_pos.y) * 0.2

    def render(self):
        self.level.render(self.camera_pos)

        controller.win.blit(controller.hud_back, (293, 28))
        self.render_hud()
        controller.win.blit(controller.hud, (0, 0))

        self.achievement_handler.draw(controller.win, self.level, controller.fonts)

game_manager = GameManager()