# fill here
import pico2d
import game_framework
import stage_middle
import logo_state
import title_state

# import item_state

pico2d.open_canvas(1280, 720)
# game_framework.run(item_state)
# game_framework.run(logo_state)
game_framework.run(logo_state)
pico2d.close_canvas()
