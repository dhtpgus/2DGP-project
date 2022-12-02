from pico2d import *
import game_world
import server
# from skul import Skul
# from skul import attack
import skul

class Skul_Attack:

    def __init__(self, x=800,y=300):
        self.x, self.y = x, y
        pass

    def draw(self):
        if skul.attack:
            draw_rectangle(*self.get_bb())
        pass

    def update(self):
        if skul.attack == False:
            game_world.remove_object(skul.s_attack)
        pass

    def get_bb(self):
        cx = self.x - server.map.window_left
        if attack and self.face_dir == 1:
            return cx - 47, self.y - 40, cx + 50, self.y + 47
        elif attack and self.face_dir == -1:
            return cx - 50, self.y - 40, cx + 47, self.y + 47
        pass

    def handle_collision(self, other, group):
        pass