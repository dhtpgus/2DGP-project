import pico2d
import game_framework
import stage_middle
import logo_state
import title_state
import stage_start
import server
import stage_boss

# import item_state
server.stage = stage_start

pico2d.open_canvas(1280, 720)
game_framework.run(logo_state)
#game_framework.run(stage_boss)
pico2d.close_canvas()
