from pico2d import *
import game_world
import game_framework
import server
import enemy

RD, LD, RU, LU, TIMER, SPACE, XD, XU = range(8)
event_name = ['RD', 'LD', 'RU', 'LU', 'TIMER', 'SPACE', 'XD', 'XU']
key_event_table = {
    (SDL_KEYDOWN, SDLK_x): XD,
    (SDL_KEYUP, SDLK_x): XU,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU
}


class IDLE:
    @staticmethod
    def enter(skul, event):
        global jumped, falling, attack, jumped_count
        if event == SPACE:
            if jumped_count < 2:
                jumped = True
                falling = False
                jumped_count += 1
            pass
        elif event == XD:
            attack = True
            skul.attack_sound1.play()
        elif event == XU:
            attack = False
        skul.dir = 0
        skul.timer = 100

    @staticmethod
    def exit(skul, event):
        pass

    @staticmethod
    def do(skul):
        global jumped, falling, jump_height, jumped_count
        skul.frame = (skul.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        # before_jumped_y = skul.y
        if jumped:
            falling = False
            skul.diry = 2
            jump_height += 2
            if jump_height % 250 == 0:
                jumped = False
        if falling:
            skul.diry = -2
            pass
        skul.y += skul.diry * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(skul):
        cx = skul.x - server.map.window_left
        if attack and skul.face_dir == -1:
            attackL_images[int(skul.frame)].draw(cx, skul.y)
        elif attack and skul.face_dir == 1:
            attackR_images[int(skul.frame)].draw(cx, skul.y)
        elif jumped and skul.face_dir == -1:
            skul.jump_image.clip_draw((int(skul.frame) // 4) * 40, 60, 40, 61, cx, skul.y - 2)
        elif jumped and skul.face_dir == 1:
            skul.jump_image.clip_draw((int(skul.frame) // 4) * 40, 0, 40, 61, cx, skul.y - 2)
        elif falling and skul.face_dir == -1:
            skul.falling_image.clip_draw((int(skul.frame) // 4) * 67, 60, 67, 60, cx, skul.y - 2)
        elif falling and skul.face_dir == 1:
            skul.falling_image.clip_draw((int(skul.frame) // 4) * 67, 0, 67, 60, cx, skul.y - 2)
        elif skul.face_dir == 1:
            skul.idle_image.clip_draw((int(skul.frame) // 2) * 77, 60, 72, 60, cx, skul.y - 2, 66, 55)
        else:
            skul.idle_image.clip_draw((int(skul.frame) // 2) * 77, 0, 72, 60, cx, skul.y, 66, 55)


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel??? 30cm
RUN_SPEED_KMPH = 40.0  # km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class RUN:
    def enter(skul, event):
        global jumped, falling, attack, jumped_count
        if event == RD:
            skul.dir += 1
        elif event == LD:
            skul.dir -= 1
        elif event == RU:
            skul.dir -= 1
        elif event == LU:
            skul.dir += 1
        elif event == SPACE:
            if jumped_count < 2:
                skul.jump_sound.play()
                jumped = True
                falling = False
                jumped_count += 1
            pass
        elif event == XD:
            attack = True
            skul.attack_sound1.play()
        elif event == XU:
            attack = False


    def exit(skul, event):
        skul.face_dir = skul.dir

    def do(skul):
        global jumped, falling, jump_height
        skul.face_dir = skul.dir
        skul.frame = (skul.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if jumped:
            falling = False
            skul.diry = 2
            jump_height += 2
            if jump_height % 250 == 0:
                jumped = False
        if falling:
            skul.diry = -2
            pass
        skul.y += skul.diry * RUN_SPEED_PPS * game_framework.frame_time
        skul.x += skul.dir * RUN_SPEED_PPS * game_framework.frame_time

        if server.boss_stage == True:
            if skul.y < 342:
                cx = 280 - server.map.window_left
                skul.x = clamp(cx + 80, skul.x, cx + 2330)
            elif 342 <= skul.y < 407:
                cx = 280 - server.map.window_left
                skul.x = clamp(cx - 60, skul.x, cx + 2330)
            elif skul.y >= 407:
                cx = 280 - server.map.window_left
                skul.x = clamp(cx - 50, skul.x, server.map.w - 1)
        else:
            skul.x = clamp(0, skul.x, server.map.w - 1)

    def draw(skul):
        cx = skul.x - server.map.window_left
        # print(skul.x, cx) # skul.x ??? cx??? ???????????
        if attack and skul.face_dir == -1:
            attackL_images[int(skul.frame)].draw(cx, skul.y)
        elif attack and skul.face_dir == 1:
            attackR_images[int(skul.frame)].draw(cx, skul.y)
        elif jumped and skul.face_dir == -1:
            skul.jump_image.clip_draw((int(skul.frame) // 4) * 40, 60, 40, 61, cx, skul.y - 2)
        elif jumped and skul.face_dir == 1:
            skul.jump_image.clip_draw((int(skul.frame) // 4) * 40, 0, 40, 61, cx, skul.y - 2)
        elif falling and skul.face_dir == -1:
            skul.falling_image.clip_draw((int(skul.frame) // 4) * 67, 60, 67, 60, cx, skul.y - 2)
        elif falling and skul.face_dir == 1:
            skul.falling_image.clip_draw((int(skul.frame) // 4) * 67, 0, 67, 60, cx, skul.y - 2)
        elif skul.dir == -1:
            skul.image.clip_draw(int(skul.frame) * 73, 0, 70, 60, cx, skul.y)
        elif skul.dir == 1:
            skul.image.clip_draw(int(skul.frame) * 73, 62, 70, 60, cx, skul.y)


jumped = False
jumped_count = 0  # ????????????????????? ???????????? ???????????? ?????? ??????
jump_height = 0  # ?????? ??????
falling = True
attack = False
attackR_images = []
attackL_images = []
skul_hp_bar = []

next_state = {
    IDLE: {RU: RUN, LU: RUN, RD: RUN, LD: RUN},
    RUN: {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE}
}


class Skul:
    def __init__(self):
        self.attack_sound1 = load_wav('./resource/AudioClip/Skul_Atk 1.wav')
        self.attack_sound1.set_volume(20)
        self.jump_sound = load_wav('./resource/AudioClip/Imp_jump 3.wav')
        self.jump_sound.set_volume(30)
        self.hit_sound = load_wav('./resource/AudioClip/Hit_sound.wav')
        self.hit_sound.set_volume(3)
        self.x, self.y = 300, 1000
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.diry = 0
        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)
        self.image = load_image('./resource/sprites/skulwalk2.png')
        self.idle_image = load_image('./resource/sprites/skulidle2.png')
        self.jump_image = load_image('./resource/sprites/skuljump2.png')
        self.falling_image = load_image('./resource/sprites/skulfall2.png')
        for i in range(1, 9):
            attackR_images.append(load_image('./resource/sprites/attack_' + '%d' % i + '.png'))
        for i in range(1, 9):
            attackL_images.append(load_image('./resource/sprites/attackL_' + '%d' % i + '.png'))
        for i in range(12):
            skul_hp_bar.append(load_image('./resource/sprites/hp_bar_' + '%d' % i + '.png'))

        self.item = None

    def update(self):
        self.cur_state.do(self)
        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                pass
                # print('ERROR', self.cur_state, 'Event', event_name[event])
                # print(f'ERROR: State {self.cur_state.__name__}  Event {event_name[event]}')
            self.cur_state.enter(self, event)
        self.x = clamp(0, self.x, server.map.w - 1)
        self.y = clamp(0, self.y, server.map.h - 1)

        # enemy ????????? ????????? ?????? ???????????? ???????????? ?????????????????? ?????? enemy2,3??????
        if server.enemy2 is not None:
            if attack == True and self.face_dir == 1:
                cx = self.x - server.map.window_left  # ??? ??????
                dx = server.enemy.x - server.map.window_left  # enemy ??????
                if not (dx - 30 > cx + 50) and not (dx + 30 < cx - 47) and not (
                        server.enemy.y + 47 < self.y - 30) and not (server.enemy.y - 45 > self.y + 30):
                    self.hit_sound.play()
                    server.enemy_attacked = True
            elif attack == True and self.face_dir == -1:
                cx = self.x - server.map.window_left  # ??? ??????
                dx = server.enemy.x - server.map.window_left  # enemy ??????
                if not (dx - 30 > cx + 47) and not (dx + 30 < cx - 50) and not (
                        server.enemy.y + 47 < self.y - 30) and not (server.enemy.y - 45 > self.y + 30):
                    self.hit_sound.play()
                    server.enemy_attacked = True
            if server.enemy_attacked:
                server.enemy.hp -= 0.1
                server.enemy_attacked = False

            if attack == True and self.face_dir == 1:
                cx = self.x - server.map.window_left  # ??? ??????
                dx = server.enemy2.x - server.map.window_left  # enemy ??????
                if not (dx - 30 > cx + 50) and not (dx + 30 < cx - 47) and not (
                        server.enemy2.y + 47 < self.y - 30) and not (server.enemy2.y - 45 > self.y + 30):
                    self.hit_sound.play()
                    server.enemy2_attacked = True
            elif attack == True and self.face_dir == -1:
                cx = self.x - server.map.window_left  # ??? ??????
                dx = server.enemy2.x - server.map.window_left  # enemy ??????
                if not (dx - 30 > cx + 47) and not (dx + 30 < cx - 50) and not (
                        server.enemy2.y + 47 < self.y - 30) and not (server.enemy2.y - 45 > self.y + 30):
                    self.hit_sound.play()
                    server.enemy2_attacked = True
            if server.enemy2_attacked:
                server.enemy2.hp -= 0.1
                server.enemy2_attacked = False

            if attack == True and self.face_dir == 1:
                cx = self.x - server.map.window_left  # ??? ??????
                dx = server.enemy3.x - server.map.window_left  # enemy ??????
                if not (dx - 30 > cx + 50) and not (dx + 30 < cx - 47) and not (
                        server.enemy3.y + 47 < self.y - 30) and not (server.enemy3.y - 45 > self.y + 30):
                    self.hit_sound.play()
                    server.enemy3_attacked = True
            elif attack == True and self.face_dir == -1:
                cx = self.x - server.map.window_left  # ??? ??????
                dx = server.enemy3.x - server.map.window_left  # enemy ??????
                if not (dx - 30 > cx + 47) and not (dx + 30 < cx - 50) and not (
                        server.enemy3.y + 47 < self.y - 30) and not (server.enemy3.y - 45 > self.y + 30):
                    self.hit_sound.play()
                    server.enemy3_attacked = True
            if server.enemy3_attacked:
                server.enemy3.hp -= 0.1
                server.enemy3_attacked = False

        if server.boss is not None:
            if attack == True and self.face_dir == 1:
                cx = self.x - server.map.window_left  # ??? ??????
                dx = server.boss.x - server.map.window_left  # enemy ??????
                if not (dx - 78 > cx + 50) and not (dx + 78 < cx - 47) and not (
                        server.boss.y + 70 < self.y - 30) and not (server.boss.y - 78 > self.y + 30):
                    self.hit_sound.play()
                    server.boss_attacked = True
            elif attack == True and self.face_dir == -1:
                cx = self.x - server.map.window_left  # ??? ??????
                dx = server.boss.x - server.map.window_left  # enemy ??????
                if not (dx - 78 > cx + 47) and not (dx + 78 < cx - 50) and not (
                        server.boss.y + 70 < self.y - 30) and not (server.boss.y - 78 > self.y + 30):
                    self.hit_sound.play()
                    server.boss_attacked = True
            if server.boss_attacked:
                server.boss.hp -= 0.1 / 2.0  # ????????? ?????? ???????????? ????????? ??????
                server.boss_attacked = False
            pass


    def draw(self):
        self.cur_state.draw(self)
        #draw_rectangle(*self.get_bb())  # tuple ?????? ????????? ????????? ?????????????????? * ??? ??????
        if attack:
            #draw_rectangle(*self.get_attack_bb())
            pass
        if server.skul_hp == 100:
            skul_hp_bar[11].draw(200, 90)
        elif 96 < server.skul_hp < 100:
            skul_hp_bar[10].draw(200, 90)
        elif 90 < server.skul_hp <= 96:
            skul_hp_bar[9].draw(200, 90)
        elif 80 < server.skul_hp <= 90:
            skul_hp_bar[8].draw(200, 90)
        elif 70 < server.skul_hp <= 80:
            skul_hp_bar[7].draw(200, 90)
        elif 60 < server.skul_hp <= 70:
            skul_hp_bar[6].draw(200, 90)
        elif 50 < server.skul_hp <= 60:
            skul_hp_bar[5].draw(200, 90)
        elif 40 < server.skul_hp <= 50:
            skul_hp_bar[4].draw(200, 90)
        elif 30 < server.skul_hp <= 40:
            skul_hp_bar[3].draw(200, 90)
        elif 15 < server.skul_hp <= 30:
            skul_hp_bar[2].draw(200, 90)
        elif 0 < server.skul_hp <= 15:
            skul_hp_bar[1].draw(200, 90)
        elif server.skul_hp <= 0:
            skul_hp_bar[0].draw(200, 90)


    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def get_bb(self):
        cx = self.x - server.map.window_left
        return cx - 33, self.y - 30, cx + 28, self.y + 30  # ????????????

    def get_attack_bb(self):
        cx = self.x - server.map.window_left
        if attack and self.face_dir == 1:
            return cx - 47, self.y - 40, cx + 50, self.y + 47
        elif attack and self.face_dir == -1:
            return cx - 50, self.y - 40, cx + 47, self.y + 47
        pass

    def handle_collision(self, other, group):
        global falling, jumped_count
        if group == 'skul:map':
            falling = False
            self.diry = 0
            self.y += 1
            jumped_count = 0
        if group == 'skul:floor1' or group == 'skul:floor2' or group == 'skul:floor3' and falling == True:
            falling = False
            self.diry = 0
            # self.dir = 0
            # self.y += 1
            jumped_count = 0
        pass
