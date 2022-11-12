from pico2d import *

import game_framework
import stage_start

image = None

def enter():
    global image
    image = load_image('Title_Art.png')
    pass

def exit():
    global image
    del image
    pass

def update():
   pass


def draw():
    clear_canvas()
    image.draw(1280 // 2, 720 // 2, 1280, 720)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(stage_start)


def pause():
    pass

def resume():
    pass




