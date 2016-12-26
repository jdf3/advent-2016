def left(dir):
    if dir == 'N': return 'W'
    if dir == 'W': return 'S'
    if dir == 'S': return 'E'
    if dir == 'E': return 'N'

def right(dir):
    if dir == 'N': return 'E'
    if dir == 'E': return 'S'
    if dir == 'S': return 'W'
    if dir == 'W': return 'N'

def part_one():
    f = open("input.txt")
    contents = f.read()
    instructions = contents.split(", ")

    direction = 'N'
    position = [0, 0]

    for ins in instructions:
        turn = ins[0]
        if turn == 'L': direction = left(direction)
        if turn == 'R': direction = right(direction)
        blocks = int(ins[1:])
        if direction == 'N': position[0] = position[0] + blocks
        if direction == 'E': position[1] = position[1] + blocks
        if direction == 'S': position[0] = position[0] - blocks
        if direction == 'W': position[1] = position[1] - blocks

    print("The final coordinates are ({0}, {1}), comprising a total distance of {2}".format(position[0], position[1], abs(position[0]) + abs(position[1])))

def part_two():
    f = open("input.txt")
    contents = f.read()
    instructions = contents.split(", ")

    direction = 'N'
    position = (0, 0)

    visited_points = set()
    visited_points.add(position)

    for ins in instructions:
        turn = ins[0]
        if turn == 'L': direction = left(direction)
        if turn == 'R': direction = right(direction)
        blocks = int(ins[1:])
        for i in range(blocks):
            if direction == 'N': position = (position[0] + 1, position[1])
            if direction == 'E': position = (position[0], position[1] + 1)
            if direction == 'S': position = (position[0] - 1, position[1])
            if direction == 'W': position = (position[0], position[1] - 1)
            if position in visited_points:
                return position
            visited_points.add(position)

part_one()

position = part_two()
print("The first location visited twice is ({0}, {1}), which is {2} blocks away.".format(position[0], position[1], abs(position[0]) + abs(position[1])))
