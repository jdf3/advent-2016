from collections import namedtuple
from heapq import heappush, heappop

# borrowed from good ol' #11 again
def astar_search(start, h_func, moves_func):
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
    return ([] if (s is None) else path(previous, previous[s]) + [s])

Searchstate = namedtuple("Searchstate", "position, special_visited")
Gridstate = namedtuple("Gridstate", "grid, special, zero")

def gen_h(gridstate, return_to_zero=False):
    grid = gridstate.grid
    special = gridstate.special
    zero = gridstate.zero
    def h(state):
        position = state.position
        special_remaining = gridstate.special - state.special_visited
        dist = 0
        for spec in special:
            if spec in special_remaining:
                dist += 1
        if return_to_zero and position != zero:
            dist += 1
        return dist
    return h

def cityblock_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def gen_moves(gridstate):
    grid = gridstate.grid
    special = gridstate.special
    def moves(state):
        position = state.position
        special_visited = state.special_visited
        for neighbor in neighbors(position):
            if neighbor in grid and grid[neighbor] != '#':
                if grid[neighbor] >= '0' and grid[neighbor] <= '9':
                    yield Searchstate(neighbor, special_visited | {neighbor})
                else:
                    yield Searchstate(neighbor, special_visited)
    return moves

def neighbors(position):
    yield (position[0] - 1, position[1])
    yield (position[0] + 1, position[1])
    yield (position[0], position[1] - 1)
    yield (position[0], position[1] + 1)

def find_shortest(grid_text, ret_to_start=False):
    lines = grid_text.strip().split('\n')

    grid = {}
    special = set()
    starting_position = None

    numbers = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            grid[(i, j)] = lines[i][j]
            if grid[(i, j)] in numbers:
                special.add((i, j))
            if grid[(i, j)] == '0':
                starting_position = (i, j)

    gridstate = Gridstate(grid, special, starting_position)
    path = astar_search(Searchstate(starting_position, frozenset({starting_position})), gen_h(gridstate, return_to_zero=ret_to_start), gen_moves(gridstate))
    return list(map(lambda l: l.position, path))

def tests():
    assert len(find_shortest("""###########
#0.1.....2#
#.#######.#
#4.......3#
###########""")) - 1 == 14
    print("Tests passed.")

def part_one():
    text = open("input.txt").read()

    path = find_shortest(text)
    print("Part one:", len(path) - 1)

def part_two():
    text = open("input.txt").read()

    path = find_shortest(text, ret_to_start=True)
    print("Part two:", len(path) - 1)

tests()
part_one()
part_two()
