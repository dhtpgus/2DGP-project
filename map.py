from pico2d import *
import chdir
import server
import gate

class Map_floor1:
    def __init__(self):
       pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def update(self):
        pass

    def get_bb(self):
        cx = 1500 - server.map.window_left
        return cx - 350, 350, cx + 300, 370

    def handle_collision(self, other, group):
        pass

class Map_floor2:
    def __init__(self):
       pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def update(self):
        pass

    def get_bb(self):
        cx = 1830 - server.map.window_left
        return cx - 350, 540, cx + 290, 560

    def handle_collision(self, other, group):
        pass

class Map:  # middleMap
    def __init__(self):
        self.image = load_image('Skulmap_middle.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        # self.image = load_image('skulmap_middle.png')

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, 0 , self.canvas_width, self.canvas_height, 0, 0)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.window_left = clamp(0, int(server.skul.x) - self.canvas_width // 2, self.w - self.canvas_width)
        # self.window_bottom = clamp(0, int(server.skul.y) - self.canvas_height // 2, self.w + self.canvas_height)
        pass

    def get_bb(self):
        return 0, 0, 1600 - 1, 170

    def handle_collision(self, other, group):
        pass

class startMap:
    def __init__(self):
        self.image = load_image('startmap.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        # self.image = load_image('skulmap_middle.png')

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, 0 , self.canvas_width, self.canvas_height, 0, 0)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.window_left = clamp(0, int(server.skul.x) - self.canvas_width // 2, self.w - self.canvas_width)
        # self.window_bottom = clamp(0, int(server.skul.y) - self.canvas_height // 2, self.w + self.canvas_height)
        pass

    def get_bb(self):
        return 0, 0, 1600 - 1, 170

    def handle_collision(self, other, group):
        pass

class bossMap:
    def __init__(self):
        self.image = load_image('bossmap.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        # self.image = load_image('skulmap_middle.png')

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, 0 , self.canvas_width, self.canvas_height, 0, 0)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.window_left = clamp(0, int(server.skul.x) - self.canvas_width // 2, self.w - self.canvas_width)
        # self.window_bottom = clamp(0, int(server.skul.y) - self.canvas_height // 2, self.w + self.canvas_height)
        pass

    def get_bb(self):
        return 0, 0, 1600 - 1, 170

    def handle_collision(self, other, group):
        pass


class bossMap_floor1:
    def __init__(self):
       pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def update(self):
        pass

    def get_bb(self):
        cx = 300 - server.map.window_left
        return cx - 70, 580, cx + 68, 590

    def handle_collision(self, other, group):
        pass


class bossMap_floor2:
    def __init__(self):
       pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def update(self):
        pass

    def get_bb(self):
        cx = 280 - server.map.window_left
        return cx - 80, 170, cx + 80, 320

    def handle_collision(self, other, group):
        pass


class bossMap_floor3:
    def __init__(self):
       pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def update(self):
        pass

    def get_bb(self):
        cx = 1930 - server.map.window_left
        return cx - 200, 170, cx + 220, 380

    def handle_collision(self, other, group):
        pass
