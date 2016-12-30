from heapq import heappush, heappop
import math

# stolen from solution 11
def astar_search(start, h_func, moves_func, max_cost=None):
    frontier = [(h_func(start), start)] # heap
    previous = {start: None}
    path_cost = {start: 0}
    visited = set()
    visited.add(start)
    while frontier:
        (f, s) = heappop(frontier)
        if h_func(s) == 0:
            return path(previous, s)
        for s2 in moves_func(s):
            new_cost = path_cost[s] + 1
            if max_cost and new_cost > max_cost: continue
            visited.add(s2)
            if s2 not in path_cost or new_cost < path_cost[s2]:
                heappush(frontier, (new_cost + h_func(s2), s2))
                path_cost[s2] = new_cost
                previous[s2] = s
    return dict(fail=True, front=len(frontier), prev=len(previous), reached=visited)

def path(previous, s):
    return [] if s is None else path(previous, previous[s]) + [s]

def gen_h_func(target_position):
    def h_func(current_position):
        return math.hypot(current_position[0] - target_position[0], current_position[1] - target_position[1])
    return h_func

def gen_moves_func(favorite_number):
    def moves_func(current_position):
        x, y = current_position
        if x > 0 and is_open(x - 1, y, favorite_number): yield (x - 1, y)
        if is_open(x + 1, y, favorite_number): yield (x + 1, y)
        if y > 0 and is_open(x, y - 1, favorite_number): yield (x, y - 1)
        if is_open(x, y + 1, favorite_number): yield (x, y + 1)
    return moves_func

# seems okay in tests
def is_open(x, y, fav):
    num = x * x + 3 * x + 2 * x * y + y + y * y + fav
    evens = 0
    while num > 0:
        evens += (num % 2)
        num >>= 1
    return not evens % 2

def tests():
    assert len(astar_search((1, 1), gen_h_func((7, 4)), gen_moves_func(10))) - 1 == 11

tests()

def part_one():
    print("Part one:", len(astar_search((1, 1), gen_h_func((31, 39)), gen_moves_func(1358))) - 1)

part_one()

def part_two():
    # I feel bad abusing A* like this...
    print("Part two:", len(astar_search((1, 1), gen_h_func((100,100)), gen_moves_func(1358), max_cost=50)['reached']))

part_two()


