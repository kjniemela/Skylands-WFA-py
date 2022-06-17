from utils import *

class SoundController:
    def __init__(self):
        self.sounds = {}
        self.music_vol_multiplier = 1

        self.sound_enabled = True
        self.music_enabled = True

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
        pygame.mixer.music.load(resource_path(path))
        self.music_vol_multiplier = vol_multiplier

    # def update_volumes(self):
    #     pygame.mixer.music.set_volume(self.)

    def play_sound(self, sound_id):
        if self.sound_enabled:
            self.sounds[sound_id][0]
            return self.sounds[sound_id][0].play()

    def play_music(self, loops=0, start=0.0, fade_ms=0):
        if self.music_enabled:
            pygame.mixer.music.set_volume(self.music_vol * self.music_vol_multiplier)
            pygame.mixer.music.set_endevent(MUSIC_END)
            pygame.mixer.music.play(loops, start, fade_ms)

    def stop_sound(self, sound_id, fadeout=None):
        if fadeout != None:
            self.sounds[sound_id][0].fadeout(fadeout)
        else:
            self.sounds[sound_id][0].stop()

    def stop_music(self, music_id, fadeout=None):
        pygame.mixer.music.set_endevent()
        if fadeout != None:
            pygame.mixer.music.fadeout(fadeout)
        else:
            pygame.mixer.music.stop()