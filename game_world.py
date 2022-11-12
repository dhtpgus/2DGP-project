world = [[], []]  # 게임 월드는 객체들의 집합

collision_group = dict()

def add_object(o, depth):
    world[depth].append(o)


def add_objects(ol, depth):
    world[depth] += ol


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    raise ValueError('Trying destroy non existing object')


def all_objects():
    for layer in world:
        for o in layer:
            yield o


def clear():
    for o in all_objects():
        del o
    for layer in world:
        layer.clear()


def add_collision_pairs(a, b, group):
    if group not in collision_group:
        print('add new group')
        collision_group[group] = [[], []]

    if a:
        if type(a) == list:
            collision_group[group][0] += a  # a가 리스트이면, 리스트 추가
        else:
            collision_group[group][0].append(a)  # 단일 오브젝트이면 추가

    if b:
        if type(b) == list:
            collision_group[group][1] += b  # a가 리스트이면, 리스트 추가
        else:
            collision_group[group][1].append(b)  # 단일 오브젝트이면 추가


def all_collision_pairs():
    for group, pairs in collision_group.items():  # key,value 를 다 가져옴
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group


def remove_collision_object(o):
    for pairs in collision_group.values():  # key 는 필요없으므로 values 만 가져온다
        if o in pairs[0]:
            pairs[0].remove(o)
        elif o in pairs[1]:
            pairs[1].remove(o)