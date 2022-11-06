from pico2d import *
import game_framework
import chdir
from skul import Skul
from map import Map
import game_world


# import item_state

skul = None
map = None


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            skul.handle_event(event)


def enter():
    global skul, map
    skul = Skul()
    map = Map()
    game_world.add_object(map, 0)
    game_world.add_object(skul, 1)


# finalization code
def exit():
   game_world.clear()


def update():
    for game_object in game_world.all_objects():
        game_object.update()

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def pause():
    pass


def resume():
    pass
