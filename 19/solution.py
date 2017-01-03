import math

def side_elf(count):
    return (count << 1) + 1 - (1 << (math.floor(math.log(count, 2) + 1)))

def part_one():
    print("Part one:", side_elf(3005290))

part_one()

def across_elf(count):
    p = 3**(math.floor(math.log(count, 3)))
    if count == p: return count
    return count - p + max(count - 2 * p,0)

def part_two():
    print("Part two:", across_elf(3005290))

part_two()
