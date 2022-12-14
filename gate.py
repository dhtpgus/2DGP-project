from pico2d import *
import game_world
import server

class Gate1:
    image = None

    def __init__(self):
        # if gate1.image == None:
        #     gate1.image = load_image('gate.png')
        self.x, self.y, = 860, 300

    def draw(self):
        # self.image.draw(self.x, self.y)
        # draw_rectangle(*self.get_bb())
        pass


    def update(self):
        server.gate_open = False
        pass

    def get_bb(self):
        cx = self.x - server.map.window_left
        return cx - 150, self.y - 130, cx + 150, self.y + 130

    def handle_collision(self, other, group):
        if group == 'skul:start_gate1':
            server.gate_open = True
            # print("collision:", group)
            pass   # 추가예정


class Gate2:
    image = None

    def __init__(self):
        # if gate1.image == None:
        #     gate1.image = load_image('gate.png')
        self.x, self.y, = 1460, 300

    def draw(self):
        # self.image.draw(self.x, self.y)
        #draw_rectangle(*self.get_bb())
        pass

    def update(self):
        server.gate_open = False

    def get_bb(self):
        cx = self.x - server.map.window_left
        return cx - 150, self.y - 130, cx + 150, self.y + 130

    def handle_collision(self, other, group):
        if group == 'skul:start_gate2':
            server.gate_open = True
            # print("collision", group)
            pass  # 추가예정


class mGate1:   # middlemap gate
    image = None

    def __init__(self):
        if self.image == None:
            self.image = load_image('./resource/sprites/gate1.png')
        self.x, self.y, = 1920, 300

    def draw(self):
        cx = self.x - 15 - server.map.window_left
        if server.enemy_count == 0:
            self.image.draw(cx, self.y + 10, 390.5, 266.2)  # 355, 242
        #draw_rectangle(*self.get_bb())

    def update(self):
        server.gate_open = False
        pass

    def get_bb(self):
        cx = self.x - server.map.window_left
        return cx - 150, self.y - 130, cx + 150, self.y + 130

    def handle_collision(self, other, group):
        if group == 'skul:mgate1':
            server.gate_open = True
            pass   # 추가예정


class mGate2:   # middlemap gate
    image = None

    def __init__(self):
        if self.image == None:
            self.image = load_image('./resource/sprites/gate2.png')
        self.x, self.y, = 2520, 300

    def draw(self):
        cx = self.x - server.map.window_left
        if server.enemy_count == 0:
            self.image.draw(cx, self.y + 10, 390.5, 266.2)  # 355, 242
        #draw_rectangle(*self.get_bb())

    def update(self):
        server.gate_open = False
        pass

    def get_bb(self):
        cx = self.x - server.map.window_left
        return cx - 150, self.y - 130, cx + 150, self.y + 130

    def handle_collision(self, other, group):
        if group == 'skul:mgate2':
            server.gate_open = True
            pass  # 추가예정



class bGate:   # bossmap gate
    image = None

    def __init__(self):
        if self.image == None:
            self.image = load_image('./resource/sprites/gate1.png')
        self.x, self.y, = 1930, 500

    def draw(self):
        cx = self.x - 20 - server.map.window_left
        if server.enemy_count == 0:
            self.image.draw(cx, self.y + 10, 390.5, 266.2)  # 355, 242
        #draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        cx = self.x - server.map.window_left
        return cx - 150, self.y - 130, cx + 150, self.y + 130

    def handle_collision(self, other, group):
        if group == 'skul:b_gate':
            pass  # 추가예정