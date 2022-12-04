from pico2d import *
import game_framework
from skul import Skul
from skul import attack
import skul
import map
from enemy import Enemy
import game_world
import gameover_state
import ending_state
import title_state
import item_state
import server
from gate import bGate
from boss import Boss

gate = None
floor1 = None
floor2 = None
floor3 = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            game_framework.push_state(item_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_f):
            game_framework.change_state(ending_state)
            pass  # 엔딩 출력
            #
        else:
            server.skul.handle_event(event)


def enter():
    server.boss_stage = True
    server.enemy_count = 1
    global gate, floor1, floor2, floor3
    gate = bGate()
    server.skul = Skul()
    server.map = map.bossMap()
    floor1 = map.bossMap_floor1()
    floor2 = map.bossMap_floor2()
    floor3 = map.bossMap_floor3()
    server.boss = Boss()
    game_world.add_object(server.map, 0)
    game_world.add_object(gate, 0)
    game_world.add_object(server.boss, 1)
    game_world.add_object(server.skul, 1)
    game_world.add_object(floor1, 0)
    game_world.add_object(floor2, 0)
    game_world.add_object(floor3, 0)
    game_world.add_collision_pairs(server.skul, server.boss, 'skul:boss')
    game_world.add_collision_pairs(server.skul, server.map, 'skul:map')
    game_world.add_collision_pairs(server.skul, floor1, 'skul:floor1')
    game_world.add_collision_pairs(server.skul, floor2, 'skul:floor2')
    game_world.add_collision_pairs(server.skul, floor3, 'skul:floor3')



# finalization code
def exit():
   game_world.clear()


def update():
    if server.skul_hp <= 0:
        game_framework.change_state(gameover_state)
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
