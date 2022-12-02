from pico2d import *
# from skul import Skul
import skul
import stage_middle
import game_framework
import math
import random
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import game_world
import server

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

attack_target = False
Enemy_run_image = []
Enemy_attack_image = []
Enemy_hp_bar = []


class Enemy:
    def prepare_patrol_points(self):
        positions = [(1250, 405), (1350, 405), (1450, 405), (1550, 405), (1650, 405), (1750, 405)]
        self.patrol_points = []
        for p in positions:
            self.patrol_points.append((p[0], p[1]))
        pass

    def __init__(self):
        self.hp = 110
        self.prepare_patrol_points()
        self.patrol_order = 1
        self.x, self.y = self.patrol_points[0]
        self.timer = 1.0
        self.wait_timer = 2.0
        self.frame = 0
        self.image = load_image('enemy.png')
        for i in range(1, 9):
            Enemy_run_image.append(load_image('enemy_run_' + '%d' % i + '.png'))
        for i in range(5):
            Enemy_attack_image.append(load_image('enemy_attack' + '%d' % i + '.png'))
        for i in range(13):
            Enemy_hp_bar.append(load_image('enemy_hp_bar' + '%d' % i + '.png'))
        self.item = None
        self.build_behavior_tree()

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.timer = 1.0
            self.dir = random.random() * 2 * math.pi
            return BehaviorTree.SUCCESS
        return BehaviorTree.SUCCESS

    def wait(self):
        self.speed = 0
        self.wait_timer -= game_framework.frame_time
        if self.wait_timer <= 0:
            self.wait_timer = 2.0
            return BehaviorTree.SUCCESS
        return BehaviorTree.SUCCESS

    def find_player(self):
        distance = (server.skul.x - self.x) ** 2 + (server.skul.y - self.y) ** 2
        if distance < (PIXEL_PER_METER * 20) ** 2 and self.y + 60 > server.skul.y > self.y - 60:  # 20미터 이내의 플레이어 감지, 자신의 y값보다 높으면 감지 못함
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL
        pass

    def move_to_player(self):
        self.speed = RUN_SPEED_PPS
        self.dir = math.atan2(server.skul.y - self.y, server.skul.x - self.x)
        return BehaviorTree.SUCCESS  # 플레이어 방향으로 이동시작하면 성공으로 간주
        pass

    def get_next_position(self):
        self.target_x, self.target_y = self.patrol_points[self.patrol_order % len(self.patrol_points)]
        self.patrol_order += 1
        self.dir = math.atan2(self.target_y - self.y, self.target_x - self.x)
        return BehaviorTree.SUCCESS
        pass

    def move_to_target(self):
        self.speed = RUN_SPEED_PPS
        distance = (self.target_x - self.x) ** 2 + (
                self.target_y - self.y) ** 2  # 두 점사이의 거리(루트는 안씌워도됌, 정확한 거리 구하는것이아니고, 루트계산이 시간아깝기때문)
        if distance < (PIXEL_PER_METER * 1.5) ** 2:  # 1.5미터 이내이면..
            return BehaviorTree.SUCCESS  # 다 왔음
        else:
            return BehaviorTree.RUNNING  # 아직 가고있음
        pass

    def attack_target(self):
        global attack_target
        distance = abs(server.skul.x - self.x)
        if distance < PIXEL_PER_METER * 1.5:
            #print('ATTACK')
            self.speed = 0
            attack_target = True
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

        pass

    def build_behavior_tree(self):
        wander_node = LeafNode('Wander', self.wander)
        wait_node = LeafNode('Wait', self.wait)
        wander_wait_node = SequenceNode('WanderWait')
        wander_wait_node.add_children(wander_node, wait_node)

        get_next_position_node = LeafNode('Get Next Position', self.get_next_position)
        move_to_target_node = LeafNode('Move to Target', self.move_to_target)
        patrol_node = SequenceNode('Patrol')
        patrol_node.add_children(get_next_position_node, move_to_target_node)

        find_player_node = LeafNode('Find Player', self.find_player)
        move_to_player_node = LeafNode('Move to Player', self.move_to_player)
        chase_node = SequenceNode('Chase')
        chase_node.add_children(find_player_node, move_to_player_node)

        chase_patrol_node = SelectorNode('Chase or Patrol')
        chase_patrol_node.add_children(chase_node, patrol_node)

        attack_node = LeafNode('Attack', self.attack_target)
        attack_chase_patrol_node = SequenceNode('Patrol or Chase and Attack')
        attack_chase_patrol_node.add_children(chase_patrol_node, attack_node)

        self.bt = BehaviorTree(attack_chase_patrol_node)

    def update(self):
        global attack_target
        attack_target = False
        self.bt.run()
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        if int(self.frame) > 4 and attack_target == True and math.cos(self.dir) > 0:  # 충돌 객체 추가해 handle_collision에서 처리하고 싶으나 오류가 자꾸 생겨서 일단 update 에서 처리
            cx = self.x - server.map.window_left
            dx = server.skul.x - server.map.window_left
            if not(dx - 33 > cx + 70) and not(dx + 28 < cx - 27) and not(server.skul.y + 30 < self.y - 30) and not(server.skul.y - 30 > self.y + 47):
                server.skul_attacked = True
        elif int(self.frame) > 4 and attack_target == True and math.cos(self.dir) <= 0:
            cx = self.x - server.map.window_left
            dx = server.skul.x - server.map.window_left
            if not (dx - 33 > cx + 27) and not (dx + 28 < cx - 70) and not (server.skul.y + 30 < self.y - 30) and not (
                    server.skul.y - 30 > self.y + 47):
                server.skul_attacked = True
        if server.skul_attacked:  # server.skul.hp 는 스테이지별로 따로 적용되서 skul.hp값을 다음 스테이지로 넘겨주거나 server에 skul_hp를 만들어주거나 해야할것같음(수정필요)
            server.skul_hp -= 0.1
            server.skul_attacked = False

        # self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        # self.x = clamp(50, self.x, 1280 - 50)
        # self.y = clamp(50, self.y, 1024 - 50)

    def draw(self):
        cx = self.x - server.map.window_left
        if math.cos(self.dir) >= 0 and attack_target == True:
            if int(self.frame) < 4:
                Enemy_attack_image[0].draw(cx, self.y)
            else:
                Enemy_attack_image[int(self.frame) - 3].draw(cx, self.y)
                draw_rectangle(*self.get_enemy_attack_bb())
        elif math.cos(self.dir) < 0 and attack_target == True:
            if int(self.frame) < 4:
                Enemy_attack_image[0].clip_composite_draw(0, 0, 103, 103, 0, 'h', cx, self.y)
            else:
                Enemy_attack_image[int(self.frame) - 3].clip_composite_draw(0, 0, 103, 103, 0, 'h', cx, self.y)
                draw_rectangle(*self.get_enemy_attack_bb())
        elif math.cos(self.dir) < 0:
            # self.image.clip_composite_draw(0, 0, 60, 90, 0, 'h', cx, self.y)
            Enemy_run_image[int(self.frame)].clip_composite_draw(0, 0, 90, 90, 0, 'h', cx, self.y)
        elif math.cos(self.dir) >= 0:
            # self.image.clip_composite_draw(0, 0, 60, 90, 0, ' ', cx, self.y)
            Enemy_run_image[int(self.frame)].draw(cx, self.y)

        if self.hp == 110:
            Enemy_hp_bar[12].draw(cx + 15, self.y - 60)
        elif 100 < self.hp < 110:
            Enemy_hp_bar[11].draw(cx + 15, self.y - 60)
        elif 90 < self.hp <= 100:
            Enemy_hp_bar[10].draw(cx + 15, self.y - 60)
        elif 80 < self.hp <= 90:
            Enemy_hp_bar[9].draw(cx + 15, self.y - 60)
        elif 70 < self.hp <= 80:
            Enemy_hp_bar[8].draw(cx + 15, self.y - 60)
        elif 60 < self.hp <= 70:
            Enemy_hp_bar[7].draw(cx + 15, self.y - 60)
        elif 50 < self.hp <= 60:
            Enemy_hp_bar[6].draw(cx + 15, self.y - 60)
        elif 45 < self.hp <= 50:
            Enemy_hp_bar[5].draw(cx + 15, self.y - 60)
        elif 35 < self.hp <= 45:
            Enemy_hp_bar[4].draw(cx + 15, self.y - 60)
        elif 25 < self.hp <= 35:
            Enemy_hp_bar[3].draw(cx + 15, self.y - 60)
        elif 15 < self.hp <= 25:
            Enemy_hp_bar[2].draw(cx + 15, self.y - 60)
        elif 0 < self.hp <= 15:
            Enemy_hp_bar[1].draw(cx + 15, self.y - 60)
        elif self.hp <= 0:
            Enemy_hp_bar[0].draw(cx + 15, self.y - 60)

        if self.hp <= 0:
            game_world.remove_object(server.enemy2)
            server.enemy_count -= 1
        draw_rectangle(*self.get_bb())

    def handle_events(self):
        pass

    def get_bb(self):
        cx = self.x - server.map.window_left
        return cx - 30, self.y - 45, cx + 30, self.y + 45

    def get_enemy_attack_bb(self):
        cx = self.x - server.map.window_left
        if attack_target and math.cos(self.dir) > 0:
            return cx - 27, self.y - 40, cx + 70, self.y + 47
        elif attack_target and math.cos(self.dir) < 0:
            return cx - 70, self.y - 40, cx + 27, self.y + 47
        pass

    def handle_collision(self, other, group):
        if group == 'skul_attack:enemy':
            game_world.remove_object(self)
        pass