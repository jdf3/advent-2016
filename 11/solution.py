from heapq import heappop, heappush
import math
from collections import namedtuple
from itertools import combinations, chain

def fs(*items):
    return frozenset(items)

def astar_search(start, h_func, moves_func):
    """
    Find a shortest sequence of states from start to a goal state (a state s with h_func(s) == 0).
    """
    frontier  = [(h_func(start), start)]
    previous  = {start: None}
    path_cost = {start: 0}
    while frontier:
        (f, s) = heappop(frontier)
        if h_func(s) == 0:
            return path(previous, s)
        for s2 in moves_func(s):
            new_cost = path_cost[s] + 1
            if s2 not in path_cost or new_cost < path_cost[s2]:
                heappush(frontier, (new_cost + h_func(s2), s2))
                path_cost[s2] = new_cost
                previous[s2] = s
    return dict(fail=True, front=len(frontier), prev=len(previous))

def path(previous, s):
    """
    Return a list of states that lead to state s, according to the previous dict.
    """
    return ([] if (s is None) else path(previous, previous[s]) + [s])

def astar_tests():
    State = namedtuple('State', 'position, walls, dimensions')

    # position is coordinate-tuple
    # grid is 2-D array
    # walls is tuple of coordinate-tuple
    def moves(state):
        position, walls, dimensions = state

        if position[0] < dimensions[0]:
            new_coord = (position[0] + 1, position[1])
            if (position, new_coord) not in walls:
                yield State(new_coord, walls, dimensions)

        if position[0] > 0:
            new_coord = (position[0] - 1, position[1])
            if (position, new_coord) not in walls:
                yield State(new_coord, walls, dimensions)

        if position[1] < dimensions[1]:
            new_coord = (position[0], position[1] + 1)
            if (position, new_coord) not in walls:
                yield State(new_coord, walls, dimensions)

        if position[1] > 0:
            new_coord = (position[0], position[1] - 1)
            if (position, new_coord) not in walls:
                yield State(new_coord, walls, dimensions)

    def h_to_10_10(state):
        position, _, _ = state
        return math.hypot(9 - position[0], 9 - position[1])

    walls = set({
        ((4, 8), (5, 8)),
        ((5, 5), (5, 6)),
        ((5, 7), (5, 8)),
        ((6, 7), (6, 8)),
        ((7, 7), (7, 8)),
        ((7, 7), (8, 7)),
        ((7, 6), (8, 6)),
        ((7, 5), (8, 5)),
        ((7, 4), (8, 4)),
        ((7, 3), (8, 3))
        })

    inverse_walls = set()
    for wall in walls:
        inverse_walls.add((wall[1], wall[0]))

    walls = walls.union(inverse_walls)
    walls = frozenset(walls)

    dimensions = (10, 10)
    position = (5, 5)
    results = astar_search(State(position, walls, dimensions), h_to_10_10, moves)
    # 10 moves means 11 states
    assert len(results) == 11

astar_tests()

State = namedtuple('State', 'elevator, floors')
legal_floors = {0, 1, 2, 3}

def moves(state):
    l, floors = state
    for l2 in {l + 1, l - 1} & legal_floors:
        reps = set()
        for combo in combos(floors[l]):
            newfloors = tuple((s | combo if i == l2 else
                               s - combo if i == state.elevator else
                               s)
                               for (i, s) in enumerate(state.floors))
            if is_legal_floor(newfloors[l]) and is_legal_floor(newfloors[l2]):
                #can_rep = gen_can_rep(newfloors[l], newfloors[l2])
                #if can_rep not in reps:
                #    reps.add(can_rep)
                yield State(l2, newfloors)

def gen_can_rep(f1, f2):
    f1_pairs, f1_m_f2_g, f1_m_solo, f1_g_solo, f1_g_f2_m, f2_pairs, f2_m_solo, f2_g_solo = [0]*8
    for k in (s[0] for s in f1 if s.endswith('M')):
        if k + 'G' in f1:
            f1_pairs += 1
        if k + 'G' in f2:
            f1_m_f2_g += 1
        else:
            f1_m_solo += 1
    for k in (s[0] for s in f1 if s.endswith('G')):
        if k + 'M' in f2:
            f1_g_f2_m += 1
        elif k + 'M' not in f1:
            f1_g_solo += 1
    for k in (s[0] for s in f2 if s.endswith('M')):
        if k + 'G' in f2:
            f2_pairs += 1
        elif k + 'G' not in f1:
            f2_m_solo += 1
    for k in (s[0] for s in f2 if s.endswith('G')):
        if k + 'M' not in f1 | f2:
            f2_g_solo += 1
    # count pairs in f1
    # count pairs in f2
    # count gen-chip pairs in f1-f2
    # count chip-gen pairs in f1-f2
    # count loner chips in f1
    # count loner chips in f2
    # count loner generators in f1
    # count loner generators in f2
    # return a tuple of these counts
    # NB: i suspect i might need to eliminate symmetry work for the solo
    # counts, since this arguably isn't symmetry... but i haven't cooked
    # up an example for when this would matter quite yet
    return (f1_pairs, f2_pairs, f1_g_f2_m, f1_m_f2_g,
            f1_m_solo, f2_m_solo, f1_g_solo, f2_g_solo)

def combos(things):
    for s in chain(combinations(things, 1), combinations(things, 2)):
        yield frozenset(s)

def is_legal_floor(floor):
    has_rtgs = any(r.endswith('G') for r in floor)
    chips = [c for c in floor if c.endswith('M')]
    return not has_rtgs or all(generator_for(c) in floor for c in chips)

def generator_for(chip):
    return chip[0] + 'G'

def h_to_top(state):
    total = sum(len(floor) * i for (i, floor) in enumerate(reversed(state.floors)))
    return math.ceil(total / 2) # Can move two items in one move.

def test():
    # 3 moves is len 4
    assert len(astar_search(State(0, (fs('RM'), fs(), fs('RG'), fs())), h_to_top, moves)) == 4

test()

def part_one():
    print("Part one:",
            len(astar_search(State(0,
                (fs('SG', 'SM', 'PG', 'PM'),
                 fs('TG', 'RG', 'RM', 'CG', 'CM'),
                 fs('TM'),
                 fs())), h_to_top, moves)) - 1)

#part_one()

def part_two():
    print("Part two:",
            len(astar_search(State(0,
                (fs('SG', 'SM', 'PG', 'PM', 'EG', 'EM', 'DG', 'DM'),
                 fs('TG', 'RG', 'RM', 'CG', 'CM'),
                 fs('TM'),
                 fs())), h_to_top, moves)) - 1)

#part_two()
