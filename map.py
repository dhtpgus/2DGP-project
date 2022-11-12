from pico2d import *
import chdir

class Map:
    def __init__(self):
        self.image = load_image('skul_map1.png')

    def draw(self):
        self.image.draw(1280 // 2, 720 // 2)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return 0, 0, 1600 - 1, 170

    def handle_collision(self, other, group):
        pass