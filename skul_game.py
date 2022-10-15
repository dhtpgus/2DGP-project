# fill here
import pico2d
import game_framework
import play_state

# import item_state


pico2d.open_canvas(1280, 720)
# game_framework.run(item_state)
game_framework.run(play_state)
pico2d.close_canvas()
