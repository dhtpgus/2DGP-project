from pico2d import *
import game_framework
import stage_middle
import title_state

running = True
image = None
gameover_time = 0.0

def enter():
    global image
    image = load_image('./resource/sprites/gameover.png')
    pass

def exit():
    global image
    del image
    pass

def update():
    global gameover_time
    # global running
    if gameover_time > 2:
        gameover_time = 0
        game_framework.quit()
    delay(0.01)
    gameover_time += 0.01
    pass

def draw():
    clear_canvas()
    image.draw(1280 // 2, 720 // 2)
    update_canvas()
    pass

def handle_events():
    events = get_events()





