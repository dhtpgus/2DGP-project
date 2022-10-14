from pico2d import *
import game_framework
# import item_state



class Map:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)


class Skul:
    def __init__(self):
        self.x, self.y = 10, 80
        self.frame = 0
        self.dir = 0
        self.image = load_image('skulwalk2.png')
        self.item = None

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir * 1
        print(self.x)
        # if self.x > 800:
        #     self.x = 800
        #     self.dir = -1  # 왼쪽
        # elif self.x < 0:
        #     self.x = 0
        #     self.dir = 1

    def draw(self):
        if L == 0 and R == 0:
            self.image.clip_draw(self.frame * 73, 62, 70, 60, self.x, self.y)
        elif R == 1:
            self.image.clip_draw(self.frame * 73, 62, 70, 60, self.x, self.y)
        elif L == 1:
            self.image.clip_draw(self.frame * 73, 0, 70, 60, self.x, self.y)

        # if self.dir == 1:
        #     self.image.clip_draw(self.frame * 73, 62, 70, 60, self.x, self.y)
        # else:
        #     self.image.clip_draw(self.frame * 73, 0, 70, 60, self.x, self.y)


L = 0
R = 0


def handle_events():
    global running
    global L, R
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RIGHT:
                skul.dir += 1
                R = 1
                L = 0
            elif event.key == SDLK_LEFT:
                skul.dir -= 1
                L = 1
                R = 0
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                skul.dir -= 1
                R = 1
                L = 0
            elif event.key == SDLK_LEFT:
                skul.dir += 1
                R = 0
                L = 1


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
