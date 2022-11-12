from pico2d import *
# from skul import Skul
import skul
import stage_middle
import game_world
import server

turn_L = False
turn_R = True


class Boss:   # boss +161%
    def __init__(self):
        self.startx, self.starty = 1400, 250
        self.x, self.y = 1400, 250
        self.sense_range = 100
        self.frame = 0
        self.dirx = 0
        self.image = load_image('boss.png')
        self.item = None

    def update(self):
        global turn_L, turn_R
        self.frame = (self.frame + 1) % 8
        # if self.x - self.sense_range < skul.x:
        #     pass
        if self.x > self.startx + 150:
            turn_L = True
            turn_R = False
        elif self.x < self.startx - 150:
            turn_R = True
            turn_L = False
        if turn_L:
            self.x -= 1
        elif turn_R:
            self.x += 1

    def draw(self):
        cx = self.x - server.map.window_left
        if turn_L:
            self.image.clip_composite_draw(0, 0, 173, 162, 0, 'h', cx, self.y)
        else:
            self.image.clip_composite_draw(0, 0, 173, 162, 0, ' ', cx, self.y)
        draw_rectangle(*self.get_bb())

    def handle_events(self):
        pass

    def get_bb(self):
        cx = self.x - server.map.window_left
        return cx - 85, self.y - 80, cx + 85, self.y + 80

    def handle_collision(self, other, group):
        if group == 'skul_attack:enemy':
            game_world.remove_object(self)
