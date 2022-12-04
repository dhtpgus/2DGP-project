from pico2d import *
import game_framework
import title_state
import server

image = None

def enter():
    global image
    image = load_image('./resource/sprites/pause.png')
    pass


def exit():
    global image
    del image
    pass


def update():
    pass


def draw():
    clear_canvas()
    server.stage.draw_world()
    image.draw(1280 // 2, 720 // 2)
    update_canvas()
    pass


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_p:
                    game_framework.pop_state()
                case pico2d.SDLK_ESCAPE:
                    game_framework.pop_state()

