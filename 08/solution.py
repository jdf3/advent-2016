import re

def part_one():
    f = open("input.txt")
    commands = f.read().strip().split('\n')

    height = 6
    width = 50
    grid = []
    for i in range(height):
        grid.append(list('.'*width))

    for command in commands:
        if command.startswith("rect "):
            rest = command[len("rect "):]
            w, h = map(int, rest.split('x'))
            rect(grid, w, h)
        elif command.startswith("rotate row "):
            rest = command[len("rotate row "):]
            row, amount = map(int, re.match(r'y=([0-9]+) by ([0-9]+)', rest).groups())
            rotate_row(grid, width, row, amount)
        elif command.startswith("rotate column "):
            rest = command[len("rotate column "):]
            column, amount = map(int, re.match(r'x=([0-9]+) by ([0-9]+)', rest).groups())
            rotate_column(grid, height, column, amount)
        else:
            assert False

    print("Part one:", pixel_count(grid, height, width))
    print("Part two:")
    pretty_print(grid)

def rect(grid, length, height):
    for i in range(height):
        for j in range(length):
            grid[i][j] = '#'

def rotate_row(grid, grid_width, row, amount):
    row_data = list(grid[row])
    for i in range(grid_width):
        grid[row][(i + amount) % grid_width] = row_data[i]
    return

def rotate_column(grid, grid_height, column, amount):
    column_data = []
    for i in range(grid_height):
        column_data.append(grid[i][column])

    for i in range(grid_height):
        grid[(i + amount) % grid_height][column] = column_data[i]
    return

def pixel_count(grid, grid_height, grid_width):
    count = 0
    for i in range(grid_height):
        for j in range(grid_width):
            if grid[i][j] == '#':
                count += 1
    return count

def pretty_print(grid):
    for i in range(len(grid)):
        print(''.join(grid[i]))

def tests():
    grid = [['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.']]

    rect(grid, 2, 3)
    assert grid == [['#', '#', '.', '.'],
                    ['#', '#', '.', '.'],
                    ['#', '#', '.', '.'],
                    ['.', '.', '.', '.']]

    rotate_row(grid, 4, 1, 3)
    assert grid == [['#', '#', '.', '.'],
                    ['#', '.', '.', '#'],
                    ['#', '#', '.', '.'],
                    ['.', '.', '.', '.']]

    rotate_column(grid, 4, 3, 3)
    assert grid == [['#', '#', '.', '#'],
                    ['#', '.', '.', '.'],
                    ['#', '#', '.', '.'],
                    ['.', '.', '.', '.']]

    rect(grid, 2, 2)
    assert grid == [['#', '#', '.', '#'],
                    ['#', '#', '.', '.'],
                    ['#', '#', '.', '.'],
                    ['.', '.', '.', '.']]

    assert pixel_count(grid, 4, 4) == 7

tests()
part_one()
