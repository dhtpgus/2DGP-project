from pico2d import *
import game_framework
import chdir
from skul import Skul
from skul import attack
import skul
from map import Map
import map
from enemy import Enemy
import game_world
import title_state
import item_state
import stage_boss
import server
from gate import mGate1, mGate2

gate1 = None
gate2 = None
floor1 = None
floor2 = None

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
            if server.gate_open:
                game_framework.change_state(stage_boss)
        else:
            server.skul.handle_event(event)
            pass


def enter():
    global gate1, gate2, floor1
    server.skul = Skul()
    server.map = Map()
    floor1 = map.Map_floor1()
    floor2 = map.Map_floor2()
    server.enemy = Enemy()
    gate1 = mGate1()
    gate2 = mGate2()
    game_world.add_object(server.map, 0)
    game_world.add_object(server.enemy, 1)
    game_world.add_object(server.skul, 1)
    game_world.add_object(gate1, 1)
    game_world.add_object(gate2, 1)
    game_world.add_object(floor1, 1)
    game_world.add_object(floor2, 1)

    game_world.add_collision_pairs(server.skul, server.enemy, 'skul:enemy')
    game_world.add_collision_pairs(attack, server.enemy, 'skul_attack:enemy')
    game_world.add_collision_pairs(server.skul, gate1, 'skul:mgate1')
    game_world.add_collision_pairs(server.skul, gate2, 'skul:mgate2')
    game_world.add_collision_pairs(server.skul, server.map, 'skul:map')
    game_world.add_collision_pairs(server.skul, floor1, 'skul:floor1')
    game_world.add_collision_pairs(server.skul, floor2, 'skul:floor2')




# finalization code
def exit():
    game_world.remove_collision_object(floor1)
    game_world.remove_collision_object(floor2)
    game_world.remove_collision_object(gate1)  # 충돌객체 삭제해주어야함
    game_world.remove_collision_object(gate2)
    game_world.clear()


def update():
    skul.falling = True
    for game_object in game_world.all_objects():
        game_object.update()

        for a, b, group in game_world.all_collision_pairs():
            if collide(a, b):
                #print("COLLISION", group)
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

    if b == server.map or floor1 or floor2:
        if la > rb: return False
        if ra < lb: return False
        if ta - 55 < bb: return False
        if ba > tb: return False

        return True
    else:
        if la > rb: return False
        if ra < lb: return False
        if ta < bb: return False
        if ba > tb: return False

        return True


