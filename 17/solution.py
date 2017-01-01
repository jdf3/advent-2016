from heapq import heappush, heappop
from hashlib import md5
from collections import namedtuple

State = namedtuple("State", "position, passcode")

# stolen from solution 11
def astar_search(start, h_func, moves_func):
    frontier = [(h_func(start), start)] # heap
    previous = {start: None}
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
    return [] if s is None else path(previous, previous[s]) + [s]

def gen_shortest_h_func(goal):
    def h_func(state):
        position, _ = state
        return goal[0] - position[0] + goal[1] - position[1]
    return h_func

def gen_moves_func(dimensions):
    dim_x, dim_y = dimensions
    def moves_func(state):
        position, passcode = state
        pos_x, pos_y = position
        h = md5(bytes(passcode, 'utf-8')).hexdigest()
        if pos_y > 0         and 'b' <= h[0] and 'f' >= h[0]:
            yield State((pos_x, pos_y - 1), passcode + 'U')
        if pos_y < dim_y - 1 and 'b' <= h[1] and 'f' >= h[1]:
            yield State((pos_x, pos_y + 1), passcode + 'D')
        if pos_x > 0         and 'b' <= h[2] and 'f' >= h[2]:
            yield State((pos_x - 1, pos_y), passcode + 'L')
        if pos_x < dim_x - 1 and 'b' <= h[3] and 'f' >= h[3]:
            yield State((pos_x + 1, pos_y), passcode + 'R')
    return moves_func

def get_shortest_path(start, passcode, dimensions):
    result = astar_search(
                State(start, passcode),
                h_func=gen_shortest_h_func(
                    (dimensions[0] - 1, dimensions[1] - 1)),
                moves_func=gen_moves_func(dimensions))
    return result[-1].passcode[len(passcode):]

def part_one_tests():
    assert get_shortest_path((0, 0), "ihgpwlah", (4, 4)) == "DDRRRD"
    assert get_shortest_path((0, 0), "kglvqrro", (4, 4)) == "DDUDRLRRUDRD"
    assert get_shortest_path((0, 0), "ulqzkmiv", (4, 4)) == "DRURDRUDDLLDLUURRDULRLDUUDDDRR"

part_one_tests()

def part_one():
    print("Part one:", get_shortest_path((0, 0), "dmypynyp", (4, 4)))

part_one()

def all_paths_bfs(start, moves_func, goal):
    coord, passcode = start
    if coord == goal:
        yield start
        return
    for state in moves_func(start):
        for path in all_paths_bfs(state, moves_func, goal):
            yield path

def get_longest_path_len(start, passcode, dimensions):
    paths = all_paths_bfs(
            State(start, passcode),
            moves_func=gen_moves_func(dimensions),
            goal=(dimensions[0] - 1, dimensions[1] - 1))

    longest_path = max(paths,
            key=lambda path: len(path.passcode) - len(passcode))

    return len(longest_path.passcode) - len(passcode)

def part_two_tests():
    assert get_longest_path_len((0, 0), "ihgpwlah", (4, 4)) == 370
    assert get_longest_path_len((0, 0), "kglvqrro", (4, 4)) == 492
    assert get_longest_path_len((0, 0), "ulqzkmiv", (4, 4)) == 830

part_two_tests()

def part_two():
    print("Part two:", get_longest_path_len((0, 0), "dmypynyp", (4, 4)))

part_two()
