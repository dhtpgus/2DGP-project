from pico2d import *
import title_music
import game_framework
import stage_start
import game_world

image = None
music = None

def enter():
    global image, music
    music = title_music.title()
    game_world.add_object(music, 0)
    image = load_image('./resource/sprites/Title_Art.png')
    pass

def exit():
    global image
    del image
    game_world.clear()
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




