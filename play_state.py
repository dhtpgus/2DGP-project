from pico2d import *
import game_framework
import chdir
from skul import Skul
from map import Map


# import item_state

skul = None
map = None
running = True


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            skul.handle_event(event)


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
