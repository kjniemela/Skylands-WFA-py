from utils import *

class SoundController:
    def __init__(self):
        self.sounds = {}
        self.tracks = {}

        self.sound_enabled = True
        self.music_enabled = False

        pygame.mixer.pre_init(44100, -16, 4, 512)
        pygame.mixer.init() ## Throws pygame.error on failure

        self.sound_vol = 0.75
        self.music_vol = 0.75

    def load_sound(self, path, vol_multiplier=1):
        sound = pygame.mixer.Sound(resource_path(path))
        sound.set_volume(vol_multiplier*self.sound_vol)
        new_sound_id = len(self.sounds)
        self.sounds[new_sound_id] = (sound, path, vol_multiplier)
        return new_sound_id

    def load_music(self, path, vol_multiplier=1):
        sound = pygame.mixer.Sound(resource_path(path))
        sound.set_volume(vol_multiplier*self.music_vol)
        new_music_id = len(self.tracks)
        self.tracks[new_music_id] = (sound, path, vol_multiplier)
        return new_music_id

    def play_sound(self, sound_id):
        if self.sound_enabled:
            return self.sounds[sound_id][0].play()

    def play_music(self, music_id):
        if self.music_enabled:
            return self.tracks[music_id][0].play()

    def stop_sound(self, sound_id, fadeout=None):
        if fadeout != None:
            self.sounds[sound_id][0].fadeout(fadeout)
        else:
            self.sounds[sound_id][0].stop()

    def stop_music(self, music_id, fadeout=None):
        if fadeout != None:
            self.tracks[music_id][0].fadeout(fadeout)
        else:
            self.tracks[music_id][0].stop()