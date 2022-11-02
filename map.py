from pico2d import *
import chdir

class Map:
    def __init__(self):
        self.image = load_image('skul_map1.png')

    def draw(self):
        self.image.draw(1280 // 2, 720 // 2)