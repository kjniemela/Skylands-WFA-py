from utils import *
from window import controller

class Level:
    def __init__(self, lvl_file, player, sounds):

        self.platforms = []
        self.overlays = []
        self.background = []
        self.backdrop = []
        self.projectiles = []
        self.entities = []
        self.item_entities = []

        self.controls = {}
        self.data = {}

        self.sounds = sounds

        self.textures = {}

        self.cutscene = None

        self.player = player

        f = open(resource_path("levels/%s.txt" % (lvl_file)))
        data = f.read().split("\n")
        f.close()
        data = [i.split(" ") for i in data]
        for line in data:
            print(line)
            if line[0] == "cutscene":
                self.cutscene = line[1]
            elif line[0] == "texture":
                self.textures[line[1]] = controller.load_texture("assets/%s" % (line[2]))
            elif line[0] == "music":
                controller.sound_ctrl.load_music("assets/%s" % (' '.join(line[2:])))

