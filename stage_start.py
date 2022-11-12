from pico2d import *
import game_framework
import chdir
from skul import Skul
from skul import attack
import map
from enemy import Enemy
import game_world
import title_state
import item_state
import stage_middle
import server
from gate import Gate1, Gate2


gate1 = None
gate2 = None


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(title_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            game_framework.push_state(item_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_f):
            game_framework.change_state(stage_middle)
        else:
            server.skul.handle_event(event)


def enter():
    global gate1, gate2
    server.skul = Skul()
    server.map = map.startMap()
    server.enemy = Enemy()
    gate1 = Gate1()
    gate2 = Gate2()

    game_world.add_object(server.map, 0)
    game_world.add_object(server.skul, 1)
    game_world.add_object(gate1, 1)
    game_world.add_object(gate2, 1)


# finalization code
def exit():
    game_world.clear()


def update():
    for game_object in game_world.all_objects():
        game_object.update()

        for a, b, group in game_world.all_collision_pairs():
            if collide(a, b):
                print("COLLISION", group)
                a.handle_collision(b, group)  # 누가와서 충돌했는지, 어떤 관계인지정보를 알려주고 객체가 알아서 처리하도록하자
                b.handle_collision(a, group)


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


def collide(a, b):
    if a == attack:
        la, ba, ra, ta = a.get_attack_bb()
        lb, bb, rb, tb = b.get_bb()
    else:
        la, ba, ra, ta = a.get_bb()
        lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True
