from itertools import permutations
from collections import namedtuple
from heapq import heappop, heappush
import re

def part_one():
    input = open("input.txt").read().strip()
    nodes = map(lambda l: tuple(map(int, l)), re.findall(r'/dev/grid/node-x(\d+)-y(\d+)\ *(\d+)T\ *(\d+)T\ *(\d+)T\ *(\d+)%', input))

    viable = 0

    for n1, n2 in permutations(nodes, 2):
        if n1[3] + n2[3] <= n2[4]:
            viable += 1

    print("Part one:", viable)

def part_two():
    input = open("input.txt").read().strip()

    Node = namedtuple('Node', 'size, used, avail')
    grid = dict()
    for node in re.findall(r'/dev/grid/node-x(\d+)-y(\d+)\ *(\d+)T\ *(\d+)T\ *(\d+)T\ *(\d+)%', input):
        grid[(int(node[0]), int(node[1]))] = Node(int(node[2]), int(node[3]), int(node[4]))

    Gridstate = namedtuple('Gridstate', 'data_position, empty_position')

    def h(grid_state):
        return grid_state.data_position[0] + grid_state.data_position[1]

    def moves(grid_state):
        for neighbor in filter(lambda l: l in grid, neighbors(grid_state.empty_position)):
            neighbor_used = grid[neighbor].used
            empty_size = grid[grid_state.empty_position].size
            if neighbor_used < empty_size:
                if grid_state.data_position == neighbor:
                    yield Gridstate(grid_state.empty_position, neighbor)
                else:
                    yield Gridstate(grid_state.data_position, neighbor)

    def neighbors(p):
        yield (p[0] - 1, p[1])
        yield (p[0] + 1, p[1])
        yield (p[0], p[1] - 1)
        yield (p[0], p[1] + 1)

    data_position = (max(x for (x, y) in grid), 0)

    for cell in grid:
        if grid[cell].used == 0:
            empty_position = cell
            break

    path = astar_search(Gridstate(data_position, empty_position), h, moves)
    print("Part two:", len(path) - 1)

# stolen from #11 again
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

part_one()
part_two()
