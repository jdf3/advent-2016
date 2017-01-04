import re

def part_one():
    f = open("input.txt")
    text = f.read()
    ranges = list(sorted(map(lambda t: (int(t[0]), int(t[1])), re.findall(r'([0-9]+)-([0-9]+)', text))))
    highest = 0
    for low, high in ranges:
        if highest >= low:
            highest = max(highest, high + 1)
        else:
            break
    print("Part one:", highest)

def get_num_allowed(text, max_num):
    ranges = list(sorted(map(lambda t: (int(t[0]), int(t[1])), re.findall(r'([0-9]+)-([0-9]+)', text))))

    covered_len = 0

    compressed_ranges = compress_ranges(ranges)
    forbidden = sum(map(lambda t: t[1] - t[0] + 1, compressed_ranges))
    allowed = max_num + 1 - forbidden
    return allowed

# assumes sorted ranges based on lowest
def compress_ranges(ranges):
    i = 0
    low, high = None, 0
    while i < len(ranges):
        l, h = ranges[i]
        if low is None:
            low = l
            high = h
            i += 1
        elif l <= high + 1:
            high = max(h, high)
            i += 1
        else:
            yield low, high
            low, high = None, 0
    if low: yield low, high

def part_two():
    text = open("input.txt").read()
    count = get_num_allowed(text, 4294967295)
    print("Part two:", count)

def tests():
    assert get_num_allowed("""5-8
0-2
4-7""", 9) == 2

tests()

part_one()
part_two()
