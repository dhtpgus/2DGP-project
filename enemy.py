from pico2d import *


# 움직이는 적 객체 생성, 적은 플레이어(skul.x,skul.y)가 sense_range안에 들어오면 플레이어가 range 안에있는동안 플레이어를 일정속도로 따라다닌다.
# 그리고 attack_range범위안에 플레이어가 들어오면 플레이어를 공격한다.
class Enemy:  # 잡몹은 y방향 이동없음
    def __init__(self):
        self.x, self.y = 800, 200
        self.frame = 0
        self.dirx = 0
        # self.image=load_image('enemy.png')
        self.item = None

    def update(self):
        global sense_range, enemy_attack
        self.frame = (self.frame + 1) % 8
        self.x += self.dirx * 1

    def draw(self):
        self.image.clip_draw((self.frame // 2) * 77, 60, 72, 60, self.x, self.y - 2, 66, 55)

    def handle_events(self):