from pico2d import *
import game_framework


# import item_state


class Map:
    def __init__(self):
        self.image = load_image('skul_map1.png')

    def draw(self):
        self.image.draw(1280 // 2,  720 // 2)


class Skul:
    def __init__(self):
        self.x, self.y = 300, 200
        self.frame = 0
        self.dirx = 0
        self.diry = 0
        self.image = load_image('skulwalk2.png')
        self.idle_image = load_image('skulidle2.png')
        self.jump_image = load_image('skuljump2.png')
        self.falling_image = load_image('skulfall2.png')
        self.item = None

    def update(self):
        global jumped, falling
        self.frame = (self.frame + 1) % 8
        self.x += self.dirx * 1
        if jumped:
            self.diry = 20
            if self.y >= 400:
                jumped = False
                falling = True
                self.diry = -20
        if not jumped:
            if self.y <= 200:  # 나중에 현재위치에 맞게 바꿔줘야함
                self.diry = 0
                falling = False
            print(self.y)
        self.y += self.diry * 1
        delay(0.025)

    def draw(self):
        if L == 0 and R == 0:
            self.idle_image.clip_draw((self.frame // 2) * 77, 60, 72, 60, self.x, self.y-2, 66, 55)
        elif jumped and R == 1:
            self.jump_image.clip_draw((self.frame // 4) * 40, 0, 40, 61, self.x, self.y - 2)
        elif jumped and L == 1:
            self.jump_image.clip_draw((self.frame // 4) * 40, 60, 40, 61, self.x, self.y - 2)
        elif falling and R == 1:
            self.falling_image.clip_draw((self.frame // 4) * 67, 0, 67, 60, self.x, self.y - 2)
        elif falling and L == 1:
            self.falling_image.clip_draw((self.frame // 4) * 67, 60, 67, 60, self.x, self.y - 2)
        elif idle == 1 and R == 1:
            self.idle_image.clip_draw((self.frame // 2) * 77, 60, 72, 60, self.x, self.y-2, 66, 55)
        elif idle == 1 and L == 1:
            self.idle_image.clip_draw((self.frame // 2) * 77, 0, 72, 60, self.x, self.y, 66, 55)
        elif R == 1:
            self.image.clip_draw(self.frame * 73, 62, 70, 60, self.x, self.y)
        elif L == 1:
            self.image.clip_draw(self.frame * 73, 0, 70, 60, self.x, self.y)



L = 0
R = 0
ilde = 1
jumped = False
falling = False


def handle_events():
    global running
    global L, R, idle
    global jumped
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RIGHT:
                skul.dirx += 20
                R = 1
                L = 0
                idle = 0
            elif event.key == SDLK_LEFT:
                skul.dirx -= 20
                L = 1
                R = 0
                idle = 0
            elif event.key == SDLK_SPACE:
                jumped = True

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                skul.dirx -= 20
                R = 1
                L = 0
                idle = 1
            elif event.key == SDLK_LEFT:
                skul.dirx += 20
                R = 0
                L = 1
                idle = 1


skul = None
map = None
running = True


def enter():
    global skul, map, running
    skul = Skul()
    map = Map()
    running = True


# finalization code
def exit():
    global skul, map
    del skul
    del map


def update():
    skul.update()


def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def draw_world():
    map.draw()
    skul.draw()


def pause():
    pass


def resume():
    pass
