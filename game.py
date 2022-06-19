from utils import *
from vec import Vec
from window import controller
from level import Level
from player import Bullet, Player

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
        self.camera_pos = Vec(-240, 0)
        self.player = Player(Vec(0, 0))
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

    def set_level(self, level_name):
        self.level = Level(level_name, self.player, controller.sounds)

    def get_cutscene(self):
        if self.level != None:
            if self.level.cutscene != None:
                return self.level.cutscene
        
        return None

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

    def player_controls(self):
        ## TODO - much of this should be shared by all humanoid entities...
        ## TODO - properly convert this to use vectors

        player = self.player
        controls = self.controls

        previous_player_pos = Vec(*player.pos)

        if not (player.walljump and player.wallJumpTime < 5):
            if controls["left"]:
                if player.vel.x > -3:
                    player.vel.x -= 0.5 if player.view.states["sneaking"] else 2
                    player.vel.x *= 0.6

                player.view.walk_frame += player.view.facing * -1

            if controls["right"]:
                if player.vel.x < 3:
                    player.vel.x += 0.5 if player.view.states["sneaking"] else 2
                    player.vel.x *= 0.6
                
                player.view.walk_frame += player.view.facing

        if player.walljump and not player.falling:
            player.walljump = False
            player.wallJumpTime = 0
        elif player.walljump:
            player.wallJumpTime += 1

        if not player.walljump and not (controls["right"] or controls["left"]):
            player.vel.x *= 0.6
        if abs(player.vel.x) < 0.01:
            player.vel.x = 0
        if player.falling and not False: ## FLIGHT CHECK HERE TODO ??
            player.vel.y -= self.level.gravity

        if False: ## FLIGHT CHECK HERE TODO ??
            if keys[controlsMap["up"]]:
                player.yVel = 5
            elif keys[controlsMap["sneak"]]:
                player.yVel = -5
            elif not  keys[pygame.K_g]:
                player.yVel *= 0.9
        else:
            if controls["jump"] and player.touching_platform and player.jumping == 0 and not player.view.states["sneaking"]:
                player.jumping = 1
                player.vel.y += 10
            elif player.touching_platform:
                if controls["sneak"] and not player.falling:
                    player.model.height_body = 36
                    player.view.states["sneaking"] = True
                elif player.view.states["sneaking"]:
                    player.model.height_body = 48
                    player.view.states["sneaking"] = False
                    player.pos.y += 12

        if controls["reset"]:
            self.level.__init__(self.level.level_name, player, controller.sounds)
        if controls["shoot"] and player.gun_cooldown == 0:
            if player.power >= 40 and not player.reload: ## TODO - these magic numbers are gunPower
                controller.sound_ctrl.play_sound(controller.sounds["player_shoot"])
                bulletspeed = 20
                player.gun_cooldown = 20
                self.level.projectiles.append(Bullet(*player.view.held_pos, player.view.aim, bulletspeed, player))
                player.power -= 40 ## TODO - magic number
                if player.power < 40:
                    player.reload = True
            else:
                controller.sound_ctrl.play_sound(controller.sounds["click"])
                player.gun_cooldown = 30

        if player.gun_cooldown > 0:
            player.gun_cooldown -= 1
        if controls["reload"] and player.gun_cooldown == 0:
                player.reload = True

        if player.reload:
            player.power += player.reload_speed
            if player.power > player.max_power:
                player.power = player.max_power
            if player.power == player.max_power:
                player.reload = False
                player.gun_cooldown = 0

        if player.pos.y < -2000:
            player.hp = 0

        if player.hp <= 0:
            player.kill()
            self.achievement_handler.trigger("StillAlive")

        self.camera_pos.x += (((player.pos.x + 5) - (480 / 2)) - self.camera_pos.x) * 0.2
        self.camera_pos.y += (((player.pos.y + 20) + (360 / 2)) - self.camera_pos.y) * 0.2

    def update(self):
        self.level.update()
        self.player_controls()

    def render(self):
        self.level.render(self.camera_pos)

        controller.win.blit(controller.hud_back, (293, 28))
        self.render_hud()
        controller.win.blit(controller.hud, (0, 0))

        self.achievement_handler.draw(controller.win, self.level, controller.fonts)

game_manager = GameManager()