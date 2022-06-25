from utils import *
from config import config
from vec import Vec
from window import controller
from platform import *

from entity.base import Entity
from entity.biped import EntityBiped
from entity.shoaldier import EntityShoaldier

# from skyscript.skyscript import SkyScript
from skyscript.interpreter import Interpreter

class Level:
    def __init__(self, game, lvl_file, sounds):
        self.game = game

        self.platforms = []
        self.overlays = []
        self.background = []
        self.backdrop = []
        self.projectiles = []
        self.entities = []
        self.item_entities = []

        self.surfaces = []

        self.controls = {}
        self.data = {}

        self.sounds = sounds
        self.textures = {}

        self.cutscene = None
        self.level_name = lvl_file

        self.player = None

        self.gravity = 0.5

        self.entity_type_map = {
            "shoaldier": EntityShoaldier ## TODO - give this its own class
        }

        self.interpreter = Interpreter(self)

        # data = [i.split(" ") for i in data]
        # for line in data:
        #     if line[0] == "cutscene":
        #         self.cutscene = line[1]
        #     elif line[0] == "texture":
        #         self.textures[line[1]] = controller.load_texture("assets/%s" % (line[2]))
        #     elif line[0] == "music":
        #         controller.sound_ctrl.load_music("assets/%s" % (' '.join(line[2:])))
        #     elif line[0] == 'plat':
        #         self.platforms.append(Platform(line[1], int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6]), line[1] != "none"))
        #         if len(line) > 7:
        #             self.controls[line[7]] = self.platforms[-1]
        #     elif line[0] == 'platc':
        #         self.platforms.append(Platform(line[1], int(line[2]) + (int(line[4])//2), int(line[3])-(int(line[5])//2), int(line[4]), int(line[5]), int(line[6]), line[1] != "none"))
        #         if len(line) > 7:
        #             self.controls[line[7]] = self.platforms[-1]
        #     elif line[0] == 'cline':
        #         self.surfaces.append(Surface(Vec(int(line[1]), int(line[2])), Vec(int(line[3]), int(line[4]))))
        #     elif line[0] == 'overlay':
        #         self.overlays.append(Platform(line[1], int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6])))
        #     elif line[0] == 'backg':
        #         self.background.append(Platform(line[1], int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6])))
        #     elif line[0] == 'backdr':
        #         self.backdrop.append(((int(line[1]), int(line[2]), int(line[3])), (int(line[4]), int(line[5]), int(line[6]), int(line[7]))))
        #     elif line[0] == 'entity':
        #         self.entities.append(self.entity_type_map[line[1]](Vec(int(line[2]), int(line[3]))))
        #         if len(line) > 4:
        #             self.controls[line[4]] = self.entities[-1]
        #     elif line[0] == 'spawn':
        #         self.player.set_spawn(int(line[1]), int(line[2]))

    def start(self):
        f = open(resource_path("levels/%s.sky" % (self.level_name)))
        data = f.read()
        f.close()

        self.interpreter.load(data)
        self.interpreter.run()

    def get_next_entity_id(self):
        return self.game.get_next_entity_id()

    def set_player(self, player):
        self.player = player
        self.entities.append(player)

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_surface(self, surface):
        self.surfaces.append(surface)

    def add_overlay(self, overlay):
        self.overlays.append(overlay)

    def add_background(self, background):
        self.background.append(background)

    def load_texture(self, name, path):
        self.textures[name] = controller.load_texture("assets/%s" % (path))

    def update(self):
        for entity in self.entities:
            ## Apply gravity - TODO should this be done elsewhere?
            entity.vel += Vec(0, -self.gravity)

            if not entity.update():
                del self.entities[self.entities.index(entity)]
                continue

            collided = False
            avg_col_vec = Vec(0, 0)
            ground_normal = Vec(0, 0)

            for surface in self.surfaces:
                verticies = entity.get_hitbox()
                correction_vec = Vec(0, 0)

                for i in range(len(verticies)):
                    p = verticies[i]
                    q = verticies[(i+1) % len(verticies)]
                    edge = (p, q)
                    intersects, intersection_point = line_collision(edge, surface.line)
                    if intersects:
                        collided = True

                        if (p - intersection_point).normalized() @ surface.normal < 0 or p == intersection_point:
                            correction_line = (p, p + (surface.normal * (q - p).magnitude()))
                            new_correction_vec = line_collision(correction_line, surface.line, seg=False)[1] - p
                        else:
                            correction_line = (q, q + (surface.normal * (q - p).magnitude()))
                            new_correction_vec = line_collision(correction_line, surface.line, seg=False)[1] - q

                        if new_correction_vec.magnitude() > correction_vec.magnitude():
                            correction_vec = new_correction_vec

                        # print(i, i+1, correction_line, p, q, intersection_point, surface.normal)


                # if correction_vec.magnitude() > 0:
                #     print(correction_vec)
                if collided:
                    if entity.vel.magnitude() >= correction_vec.magnitude():
                        entity.pos += correction_vec
                        avg_col_vec = (avg_col_vec + correction_vec).normalized()

            if collided:
                # print(entity.vel, -avg_col_vec, entity.vel.normalized() @ -avg_col_vec)
                # print(avg_col_vec * (entity.vel.magnitude() * (entity.vel.normalized() @ -avg_col_vec)))
                ground_normal = avg_col_vec * max((entity.vel.magnitude() * (entity.vel.normalized() @ -avg_col_vec)), 0)
                entity.vel += ground_normal

                ## Friction - TODO
                entity.vel.x *= 0.6
            else:
                entity.vel.x *= 0.925

            entity.touching_platform = collided
            entity.ground_normal = ground_normal
                

        for projectile in self.projectiles:
            if not projectile.update(): ## TODO or projectile.get_touching(self):
                del self.projectiles[self.projectiles.index(projectile)]
                continue

            for surface in self.surfaces:
                pass
                ## collision logic here

    def render(self, camera_pos):
        win = controller.win
        ## TODO - refactor code so that these are not needed
        camX, camY = camera_pos

        for backdr in self.backdrop:
            if distance(*self.player.pos, backdr[1][0], backdr[1][1]) < max(backdr[1][2]/2, backdr[1][3]/2)+240:
                pygame.draw.rect(win, backdr[0], (backdr[1][0]-camX-backdr[1][2]/2, -(backdr[1][1]-camY)-backdr[1][3]/2, *backdr[1][2:]))

        for backg in self.background:
            if (self.player.pos - backg.center).magnitude() < max(backg.w/2, backg.h/2)+400:
                win.blit(self.textures[backg.texture], (backg.top_left - camera_pos).screen_coords())

        for platform in self.platforms:
            if platform.visible:
                if distance(*self.player.pos, platform.x, platform.y) < max(platform.w/2, platform.h/2)+240:
                    if platform.d == 0:
                        win.blit(self.textures[platform.texture], (platform.x-(platform.w/2)-camX, -(platform.y+(platform.h/2)-camY)))
                    else:
                        blitRotateCenter(win, self.textures[platform.texture], platform.d, (platform.x-(platform.w/2),-(platform.y+(platform.h/2))), (camX,camY))

        for entity in self.entities:
            entity.render(camera_pos)

        for projectile in self.projectiles:
            start_pos = projectile.pos - camera_pos
            end_pos = (projectile.pos + projectile.vel) - camera_pos
            pygame.draw.line(win, (83, 191, 179, 0.1), start_pos.screen_coords(), end_pos.screen_coords(), 5)
            # blitRotateCenter(win, bullet, projectile.d, (projectile.x-6,-projectile.y-3), (camX,camY))

        for overlay in self.overlays:
            if (self.player.pos - overlay.center).magnitude() < max(overlay.w/2, overlay.h/2)+400:
                win.blit(self.textures[overlay.texture], (overlay.top_left - camera_pos).screen_coords())
        
        ## TODO - debug rendering
        if config["debug"]:
            for surface in self.surfaces:
                pygame.draw.line(win, (0, 0, 0, 0.5), (surface.p-camera_pos).screen_coords(), (surface.q-camera_pos).screen_coords(), 5)
