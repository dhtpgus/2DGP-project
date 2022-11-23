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
FRAMES_PER_ACTION = 10



turn_L = False
turn_R = True

# 움직이는 적 객체 생성, 적은 플레이어(skul.x,skul.y)가 sense_range안에 들어오면 플레이어가 range 안에있는동안 플레이어를 일정속도로 따라다닌다.
# 그리고 attack_range범위안에 플레이어가 들어오면 플레이어를 공격한다.
class Enemy:  # 잡몹은 y방향 이동없음

    def prepare_patrol_points(self):
        positions = [(1200, 215), (1300, 215), (1400,215), (1500,215), (1600,215), (1700, 215)]
        self.patrol_points = []
        for p in positions:
            self.patrol_points.append((p[0], p[1]))
        pass
    def __init__(self):
        self.prepare_patrol_points()
        self.patrol_order = 1
        self.x, self.y = self.patrol_points[0]
        self.timer = 1.0
        self.wait_timer = 2.0
        self.frame = 0
        self.image = load_image('enemy.png')
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
        distance = (server.skul.x - self.x)**2 + (server.skul.y-self.y)**2
        if distance < (PIXEL_PER_METER*20)**2:  # 20미터 이내의 플레이어 감지
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL
        pass

    def move_to_player(self):
        self.speed = RUN_SPEED_PPS
        self.dir = math.atan2(server.skul.y - self.y, server.skul.x - self.x)
        return BehaviorTree.SUCCESS
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
        if distance < PIXEL_PER_METER ** 2: # 1미터 이내이면..
            return BehaviorTree.SUCCESS  # 다 왔음
        else:
            return BehaviorTree.RUNNING  # 아직 가고있음
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

        find_player_node = LeafNode('Find Player',self.find_player)
        move_to_player_node = LeafNode('Move to Player',self.move_to_player)
        chase_node = SequenceNode('Chase')
        chase_node.add_children(find_player_node, move_to_player_node)

        chase_patrol_node = SelectorNode('Chase or Patrol')
        chase_patrol_node.add_children(chase_node, patrol_node)

        #attack_chase_patrol_node = SelectorNode() # 공격 ai 만들어야함

        self.bt = BehaviorTree(chase_patrol_node)

    def update(self):
        self.bt.run()
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        # self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        # self.x = clamp(50, self.x, 1280 - 50)
        # self.y = clamp(50, self.y, 1024 - 50)

    def draw(self):
        cx = self.x - server.map.window_left
        if math.cos(self.dir) < 0:
                self.image.clip_composite_draw(0, 0, 60, 90, 0, 'h', cx, self.y)
        else:
                self.image.clip_composite_draw(0, 0, 60, 90, 0, ' ', cx, self.y)

        draw_rectangle(*self.get_bb())

    def handle_events(self):
        pass

    def get_bb(self):
        cx = self.x - server.map.window_left
        return cx - 30, self.y - 45, cx + 30, self.y + 45

    def handle_collision(self, other, group):
        if group == 'skul_attack:enemy':
            game_world.remove_object(self)