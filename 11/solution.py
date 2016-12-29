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
        for combo in combos(floors[l]):
            newfloors = tuple((s | combo if i == l2 else
                               s - combo if i == state.elevator else
                               s)
                               for (i, s) in enumerate(state.floors))
            if legal_floor(newfloors[l]) and legal_floor(newfloors[l2]):
                yield State(l2, newfloors)

def combos(things):
    for s in chain(combinations(things, 1), combinations(things, 2)):
        yield frozenset(s)

def legal_floor(floor):
    """
    Floor is legal iff no RTG or every chip has its corresponding RTG
    """
    has_rtgs = any(r.endswith('G') for r in floor)
    chips = [c for c in floor if c.endswith('M')]
    return not has_rtgs or all(generator_for(c) in floor for c in chips)

def generator_for(chip): return chip[0] + 'G'

def h_to_top(state):
    """
    An estimate of the number of moves needed to move everything to top.
    """
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

part_one()

def part_two():
    print("Part two:",
            len(astar_search(State(0,
                (fs('SG', 'SM', 'PG', 'PM', 'EG', 'EM', 'DG', 'DM'),
                 fs('TG', 'RG', 'RM', 'CG', 'CM'),
                 fs('TM'),
                 fs())), h_to_top, moves)) - 1)

part_two()
