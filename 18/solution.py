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

#part_one_tests()

def part_one():
    print("Part one:", count_safe_tiles(gen_rows([0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1], 40)))

#part_one()

# This introduces some performance issues, but still runs in a reasonable
# amount of time. A nicer solution would represent a row using just an integer
# and bit operations, and wouldn't keep the entire grid in memory - just the
# last row and a running count would suffice.
def part_two():
    print("Part two:", count_safe_tiles(gen_rows([0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1], 400000)))

#part_two()

# On second thought... perhaps a better optimization would be to look for
# cycles when generating the grid!
# Let's combine all these optimizations and see how much time we can cut down...
# Just to make sure the nuts and bolts are correct, let's do it first without
# cycle detection
#@profile - line_profiler
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

    mask = 2**columns - 1
    for i in range(1, total_rows):
        new_int_rep = ((int_rep >> 1) ^ (int_rep << 1)) & mask
        safe_count += bin(new_int_rep).count("0")
        int_rep = new_int_rep
    return safe_count

def optimization_tests():
    assert count_safe_tiles_no_cycle_detection("..^^.", 3) == 6
    assert count_safe_tiles_no_cycle_detection(".^^.^.^^^^", 10) == 38
    print("Optimization tests passed.")

#optimization_tests()

def part_two_with_optimization():
    print("Part two with optimization:", count_safe_tiles_no_cycle_detection(".^.^..^......^^^^^...^^^...^...^....^^.^...^.^^^^....^...^^.^^^...^^^^.^^.^.^^..^.^^^..^^^^^^.^^^..^", 400000))

#part_two_with_optimization()

def count_safe_tiles_cycle_detection(first_row, total_rows):
    int_rep = 0
    columns = len(first_row)
    safe_count = 0

    seen_patterns = dict()

    for char in first_row:
        int_rep <<= 1
        if char == '^':
            int_rep += 1
        else:
            safe_count += 1

    # exploit symmetry, and accommodate our endian-swapping nature of the loop
    seen_patterns[min(2**columns - int_rep, int_rep)] = (1, safe_count)

    i = 2
    mask = 2**columns - 1
    while i <= total_rows:
        mask = 2**columns - 1
        new_int_rep = ((int_rep >> 1) ^ (int_rep << 1)) & mask
        safe_count += bin(new_int_rep).count("0")
        int_rep = new_int_rep

        min_int_rep = min(2**columns - int_rep, int_rep)
        #print(min_int_rep)
        if min_int_rep in seen_patterns:

            prev_pos, prev_count = seen_patterns[min_int_rep]
            cycle_length = i - prev_pos
            cycle_safe_count = safe_count - prev_count
            num_cycles_remaining = (total_rows - i) // cycle_length
            i += cycle_length * num_cycles_remaining + 1
            safe_count += cycle_safe_count * num_cycles_remaining
            print("Skipped", cycle_length * num_cycles_remaining + 1)
        else:
            seen_patterns[min_int_rep] = (i, safe_count)
            i += 1
    return safe_count

def cycle_optimization_tests():
    assert count_safe_tiles_cycle_detection("..^^.", 3) == 6
    assert count_safe_tiles_cycle_detection(".^^.^.^^^^", 10) == 38
    print("Cycle optimization tests passed.")

#cycle_optimization_tests()

def part_two_with_cycle_optimization():
    print("Part two with cycle optimization:", count_safe_tiles_cycle_detection(".^.^..^......^^^^^...^^^...^...^....^^.^...^.^^^^....^...^^.^^^...^^^^.^^.^.^^..^.^^^..^^^^^^.^^^..^", 400000))

#part_two_with_optimization()

import cProfile

#cProfile.run('part_two()')
"""
         400007 function calls in 23.109 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   23.109   23.109 <string>:1(<module>)
        1   19.782   19.782   19.820   19.820 solution.py:20(gen_rows)
        1    3.191    3.191    3.191    3.191 solution.py:32(count_safe_tiles)
        1    0.097    0.097   23.109   23.109 solution.py:55(part_two)
        1    0.000    0.000   23.109   23.109 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
   399999    0.038    0.000    0.038    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
"""

#cProfile.run('part_two_with_optimization()')
"""
         800005 function calls in 0.815 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.815    0.815 <string>:1(<module>)
        1    0.362    0.362    0.815    0.815 solution.py:66(count_safe_tiles_no_cycle_detection)
        1    0.000    0.000    0.815    0.815 solution.py:93(part_two_with_optimization)
   399999    0.193    0.000    0.193    0.000 {built-in method builtins.bin}
        1    0.000    0.000    0.815    0.815 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
   399999    0.260    0.000    0.260    0.000 {method 'count' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
"""

cProfile.run('part_two_with_cycle_optimization()')
# This takes longer, presumably because we didn't find a cycle
"""
        1200005 function calls in 1.785 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    1.785    1.785 <string>:1(<module>)
        1    0.088    0.088    1.785    1.785 solution.py:146(part_two_with_cycle_optimization)
        1    1.091    1.091    1.697    1.697 solution.py:98(count_safe_tiles_cycle_detection)
   399999    0.174    0.000    0.174    0.000 {built-in method builtins.bin}
        1    0.000    0.000    1.785    1.785 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.len}
   400000    0.156    0.000    0.156    0.000 {built-in method builtins.min}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
   399999    0.276    0.000    0.276    0.000 {method 'count' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
"""

# Remarkably, there weren't any cycles in my input! I checked...

# Just to make sure I'm not going crazy, let's try a short input with lots rows:
#cProfile.run('print(count_safe_tiles_no_cycle_detection("..^^.", 1000000))')
"""
         2000004 function calls in 1.135 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    1.135    1.135 <string>:1(<module>)
        1    0.802    0.802    1.135    1.135 solution.py:66(count_safe_tiles_no_cycle_detection)
   999999    0.109    0.000    0.109    0.000 {built-in method builtins.bin}
        1    0.000    0.000    1.135    1.135 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
   999999    0.224    0.000    0.224    0.000 {method 'count' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
"""

#cProfile.run('print(count_safe_tiles_cycle_detection("..^^.", 1000000))')
"""
         31 function calls in 0.000 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 solution.py:98(count_safe_tiles_cycle_detection)
        7    0.000    0.000    0.000    0.000 {built-in method builtins.bin}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        8    0.000    0.000    0.000    0.000 {built-in method builtins.min}
        4    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        7    0.000    0.000    0.000    0.000 {method 'count' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
"""
