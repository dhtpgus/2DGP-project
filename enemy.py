from pico2d import *
# from skul import Skul
import skul
import stage_middle
import game_world
import server



turn_L = False
turn_R = True

# 움직이는 적 객체 생성, 적은 플레이어(skul.x,skul.y)가 sense_range안에 들어오면 플레이어가 range 안에있는동안 플레이어를 일정속도로 따라다닌다.
# 그리고 attack_range범위안에 플레이어가 들어오면 플레이어를 공격한다.
class Enemy:  # 잡몹은 y방향 이동없음
    def __init__(self):
        self.startx, self.starty = 1500, 215
        self.x, self.y = 1500, 215
        self.sense_range = 100
        self.frame = 0
        self.dirx = 0
        self.image = load_image('enemy.png')
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
            self.image.clip_composite_draw(0, 0, 60, 90, 0, 'h', cx, self.y)
        else:
            self.image.clip_composite_draw(0, 0, 60, 90, 0, ' ', cx, self.y)
        draw_rectangle(*self.get_bb())

    def handle_events(self):
        pass

    def get_bb(self):
        cx = self.x - server.map.window_left
        return cx - 30, self.y - 45, cx + 30, self.y + 45

    def handle_collision(self, other, group):
        if group == 'skul_attack:enemy':
            game_world.remove_object(self)