"""
This instruction:

"Then, a new tile is a trap only in one of the following situations:

Its left and center tiles are traps, but its right tile is not.
Its center and right tiles are traps, but its left tile is not.
Only its left tile is a trap.
Only its right tile is a trap."

Is equivalent to:

One and only one of the right and left tiles are traps

For a solution, let's use 2-D arrays, and let's use 0 for safe tiles,
and 1 for traps. For each row, add a new row to our 2-D array - then any column
is the exclusive-or of the above-left and above-right tiles.
"""

def gen_rows(first_row, total_rows):
    columns = len(first_row)
    assert columns > 1
    grid = [first_row]
    for i in range(1, total_rows):
        grid.append(list([0]*columns))
        grid[i][0] = grid[i-1][1]
        grid[i][columns - 1] = grid[i-1][columns - 2]
        for j in range(1, columns - 1):
            grid[i][j] = grid[i-1][j-1] ^ grid[i-1][j+1]
    return grid

def count_safe_tiles(grid):
    safe = 0
    for row in grid:
        for cell in row:
            safe += not cell
    return safe

def part_one_tests():
    assert count_safe_tiles(gen_rows([0, 0, 1, 1, 0], 3)) == 6
    assert count_safe_tiles(gen_rows([0, 1, 1, 0, 1, 0, 1, 1, 1, 1], 10)) == 38
    print("Part one tests passed.")

part_one_tests()

def part_one():
    print("Part one:", count_safe_tiles(gen_rows([0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1], 40)))

part_one()

# This introduces some performance issues, but still runs in a reasonable
# amount of time. A nicer solution would represent a row using just an integer
# and bit operations, and wouldn't keep the entire grid in memory - just the
# last row and a running count would suffice.
def part_two():
    print("Part one:", count_safe_tiles(gen_rows([0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1], 400000)))

#part_two()

# On second thought... perhaps a better optimization would be to look for
# cycles when generating the grid!
# Let's combine all these optimizations and see how much time we can cut down...
# Just to make sure the nuts and bolts are correct, let's do it first without
# cycle detection
def count_safe_tiles_no_cycle_detection(first_row, total_rows):
    int_rep = 0
    columns = len(first_row)
    safe_count = 0

    for char in first_row:
        int_rep <<= 1
        if char == '^':
            int_rep += 1
        else:
            safe_count += 1
    #print("{0:>10b}".format(int_rep), safe_count)

    # Note that this doesn't preserve endian-ness of the representation, but
    # we don't care, since the counts are preserved.
    for i in range(total_rows - 1):
        new_int_rep = 0
        new_int_rep = (int_rep >> 1) % 2
        safe_count += not new_int_rep

        for j in range(1, columns):
            new_int_rep <<= 1
            is_trap = (int_rep % 2) ^ ((int_rep >> 2) % 2)
            new_int_rep += is_trap
            safe_count += not is_trap

            int_rep >>= 1
        int_rep = new_int_rep
        #print("{0:>10b}".format(int_rep), safe_count)
    return safe_count

def optimization_tests():
    assert count_safe_tiles_no_cycle_detection("..^^.", 3) == 6
    assert count_safe_tiles_no_cycle_detection(".^^.^.^^^^", 10) == 38
    print("Optimization tests passed.")

optimization_tests()

def part_two_with_optimization():
    print("Part two with optimization:", count_safe_tiles_no_cycle_detection(".^.^..^......^^^^^...^^^...^...^....^^.^...^.^^^^....^...^^.^^^...^^^^.^^.^.^^..^.^^^..^^^^^^.^^^..^", 400000))

part_two_with_optimization()
