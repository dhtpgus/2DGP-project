from pico2d import *
import chdir
import game_world

RD, LD, RU, LU, TIMER, SPACE, XD, XU = range(8)
event_name = ['RD', 'LD', 'RU', 'LU', 'TIMER', 'SPACE', 'FALL']
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
    def enter(self, event):
        global jumped, attack
        print('ENTER IDLE')
        if event == SPACE:
            jumped = True
        elif event == XD:
            attack = True
        elif event == XU:
            attack = False
        self.dir = 0
        self.timer = 100

    @staticmethod
    def exit(self, event):
        print('EXIT IDLE')
        # if event == SPACE:
        #     self.fire_ball()

    @staticmethod
    def do(self):
        global jumped, falling
        self.frame = (self.frame + 1) % 8
        if jumped:
            self.diry = 2
            if self.y >= 400:
                jumped = False
                falling = True
                self.diry = -2
        if not jumped:
            if self.y <= 200:  # 나중에 현재위치에 맞게 바꿔줘야함
                self.diry = 0
                falling = False
        self.y += self.diry * 1
        # self.timer -= 1
        # if self.timer == 0:
        #     print('timer 0')
        #     self.add_event(TIMER)

    @staticmethod
    def draw(self):
        if attack and self.face_dir == -1:
            attackL_images[self.frame].draw(self.x, self.y)
        elif attack and self.face_dir == 1:
            attackR_images[self.frame].draw(self.x, self.y)
        elif jumped and self.face_dir == -1:
            self.jump_image.clip_draw((self.frame // 4) * 40, 60, 40, 61, self.x, self.y - 2)
        elif jumped and self.face_dir == 1:
            self.jump_image.clip_draw((self.frame // 4) * 40, 0, 40, 61, self.x, self.y - 2)
        elif falling and self.face_dir == -1:
            self.falling_image.clip_draw((self.frame // 4) * 67, 60, 67, 60, self.x, self.y - 2)
        elif falling and self.face_dir == 1:
            self.falling_image.clip_draw((self.frame // 4) * 67, 0, 67, 60, self.x, self.y - 2)
        elif self.face_dir == 1:
            self.idle_image.clip_draw((self.frame // 2) * 77, 60, 72, 60, self.x, self.y - 2, 66, 55)
        else:
            self.idle_image.clip_draw((self.frame // 2) * 77, 0, 72, 60, self.x, self.y, 66, 55)


class RUN:
    def enter(self, event):
        global jumped, falling, attack
        print('ENTER RUN')
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1
        elif event == SPACE:
            jumped = True
        elif event == XD:
            attack = True
        elif event == XU:
            attack = False

    def exit(self, event):
        print('EXIT RUN')
        self.face_dir = self.dir
        # if event == SPACE:
        #     self.fire_ball()

    def do(self):
        global jumped, falling
        self.face_dir = self.dir
        self.frame = (self.frame + 1) % 8
        if jumped:
            self.diry = 2
            if self.y >= 400:
                jumped = False
                falling = True
                self.diry = -2
        if not jumped:
            if self.y <= 200:  # 나중에 현재위치에 맞게 바꿔줘야함
                self.diry = 0
                falling = False
        self.y += self.diry * 1
        self.x += self.dir
        self.x = clamp(0, self.x, 1200)

    def draw(self):
        if attack and self.face_dir == -1:
            attackL_images[self.frame].draw(self.x, self.y)
        elif attack and self.face_dir == 1:
            attackR_images[self.frame].draw(self.x, self.y)
        elif jumped and self.face_dir == -1:
            self.jump_image.clip_draw((self.frame // 4) * 40, 60, 40, 61, self.x, self.y - 2)
        elif jumped and self.face_dir == 1:
            self.jump_image.clip_draw((self.frame // 4) * 40, 0, 40, 61, self.x, self.y - 2)
        elif falling and self.face_dir == -1:
            self.falling_image.clip_draw((self.frame // 4) * 67, 60, 67, 60, self.x, self.y - 2)
        elif falling and self.face_dir == 1:
            self.falling_image.clip_draw((self.frame // 4) * 67, 0, 67, 60, self.x, self.y - 2)
        elif self.dir == -1:
            self.image.clip_draw(self.frame * 73, 0, 70, 60, self.x, self.y)
        elif self.dir == 1:
            self.image.clip_draw(self.frame * 73, 62, 70, 60, self.x, self.y)


# L = 0
# R = 0
# ilde = 1
jumped = False
falling = False
attack = False
attackR_images = []
attackL_images = []

next_state = {
    IDLE: {RU: RUN, LU: RUN, RD: RUN, LD: RUN},
    RUN: {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE}
    # JUMP: {RU: JUMP, LU: JUMP, RD: JUMP, LD: JUMP, SPACE: JUMP, TIMER: IDLE}
    # FALL: {RU: FALL, LU: FALL, RD: FALL, LD: FALL, TIMER: RUN}
}


class Skul:
    def __init__(self):
        global attackR_images
        self.x, self.y = 300, 200
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        # self.dirx = 0
        # self.diry = 0
        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)
        self.image = load_image('skulwalk2.png')
        self.idle_image = load_image('skulidle2.png')
        self.jump_image = load_image('skuljump2.png')
        self.falling_image = load_image('skulfall2.png')
        attackR_images.append(load_image('attack_1.png'))
        attackR_images.append(load_image('attack_2.png'))
        attackR_images.append(load_image('attack_3.png'))
        attackR_images.append(load_image('attack_4.png'))
        attackR_images.append(load_image('attack_5.png'))
        attackR_images.append(load_image('attack_6.png'))
        attackR_images.append(load_image('attack_7.png'))
        attackR_images.append(load_image('attack_8.png'))
        attackL_images.append(load_image('attackL_1.png'))
        attackL_images.append(load_image('attackL_2.png'))
        attackL_images.append(load_image('attackL_3.png'))
        attackL_images.append(load_image('attackL_4.png'))
        attackL_images.append(load_image('attackL_5.png'))
        attackL_images.append(load_image('attackL_6.png'))
        attackL_images.append(load_image('attackL_7.png'))
        attackL_images.append(load_image('attackL_8.png'))

        self.item = None

    def update(self, event_name=None):
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
        # global jumped, falling, attack, idle
        # self.frame = (self.frame + 1) % 8
        # self.x += self.dirx * 1
        # if jumped:
        #     self.diry = 20
        #     if self.y >= 400:
        #         jumped = False
        #         falling = True
        #         self.diry = -20
        # if not jumped:
        #     if self.y <= 200:  # 나중에 현재위치에 맞게 바꿔줘야함
        #         self.diry = 0
        #         falling = False
        # self.y += self.diry * 1
        # delay(0.025)

    def draw(self):
        self.cur_state.draw(self)
        # if L == 0 and R == 0:
        #     self.idle_image.clip_draw((self.frame // 2) * 77, 60, 72, 60, self.x, self.y - 2, 66, 55)
        # elif attack and R == 1:
        #     attackR_images[self.frame].draw(self.x, self.y)
        #     delay(0.01)
        # elif attack and L == 1:
        #     attackL_images[self.frame].draw(self.x, self.y)
        #     delay(0.01)
        # elif jumped and R == 1:
        #     self.jump_image.clip_draw((self.frame // 4) * 40, 0, 40, 61, self.x, self.y - 2)
        # elif jumped and L == 1:
        #     self.jump_image.clip_draw((self.frame // 4) * 40, 60, 40, 61, self.x, self.y - 2)
        # elif falling and R == 1:
        #     self.falling_image.clip_draw((self.frame // 4) * 67, 0, 67, 60, self.x, self.y - 2)
        # elif falling and L == 1:
        #     self.falling_image.clip_draw((self.frame // 4) * 67, 60, 67, 60, self.x, self.y - 2)
        # elif idle == 1 and R == 1:
        #     self.idle_image.clip_draw((self.frame // 2) * 77, 60, 72, 60, self.x, self.y - 2, 66, 55)
        # elif idle == 1 and L == 1:
        #     self.idle_image.clip_draw((self.frame // 2) * 77, 0, 72, 60, self.x, self.y, 66, 55)
        # elif R == 1:
        #     self.image.clip_draw(self.frame * 73, 62, 70, 60, self.x, self.y)
        # elif L == 1:
        #     self.image.clip_draw(self.frame * 73, 0, 70, 60, self.x, self.y)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        # global running
        # global L, R, idle
        # global jumped, attack
        # if event.type == SDL_KEYDOWN:
        #     if event.key == SDLK_RIGHT:
        #         self.dirx += 20
        #         R = 1
        #         L = 0
        #         idle = 0
        #     elif event.key == SDLK_LEFT:
        #         self.dirx -= 20
        #         L = 1
        #         R = 0
        #         idle = 0
        #     elif event.key == SDLK_SPACE:
        #         jumped = True
        #     elif event.key == SDLK_x:
        #         attack = True
        # elif event.type == SDL_KEYUP:
        #     if event.key == SDLK_RIGHT:
        #         self.dirx -= 20
        #         R = 1
        #         L = 0
        #         idle = 1
        #     elif event.key == SDLK_LEFT:
        #         self.dirx += 20
        #         R = 0
        #         L = 1
        #         idle = 1
        #     elif event.key == SDLK_x:
        #         attack = False
