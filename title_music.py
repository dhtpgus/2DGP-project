from pico2d import *
import game_framework
import stage_start


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



class title:

    def __init__(self):
        self.bgm = load_music('./resource/AudioClip/MainTitle.wav')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def draw(self):
        pass

    def update(self):
        pass

    def get_bb(self):
        pass

    def handle_collision(self, other, group):
        pass
