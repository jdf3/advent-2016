import re

def part_one():
    f = open("input.txt")
    data = f.read().strip()
    #decompressed = decompress(data)
    #print("Part one:", len(decompressed))
    print("Part one:", better_decompressed_len(data))

def decompress(string):
    decompressed = ""
    remaining = string
    match = re.search(r"\(([0-9]+)x([0-9]+)\)", remaining)
    while match:
        num_characters, repeat_times = map(int, match.groups())
        decompressed += remaining[:match.start()]
        remaining = remaining[match.end():]
        characters_to_repeat = remaining[:num_characters]
        decompressed += characters_to_repeat * repeat_times
        remaining = remaining[num_characters:]
        match = re.search(r"\(([0-9]+)x([0-9]+)\)", remaining)
    decompressed += remaining
    return decompressed

def part_two():
    f = open("input.txt")
    data = f.read().strip()
    decompressed = decompressed_len_v2(data)
    print("Part two:", decompressed)

# This was a little interesting.
def decompressed_len_v2(string):
    matcher = re.compile(r'\(([0-9]+)x([0-9]+)\)').match

    decompressed_len = 0
    i = 0
    while i < len(string):
        m = matcher(string, i)
        if m:
            num_characters, repeat_times = map(int, m.groups())
            i = m.end(0)
            decompressed_len += repeat_times * decompressed_len_v2(string[i:i+num_characters])
            i += num_characters
        else:
            decompressed_len += 1
            i += 1
    return decompressed_len

def better_decompressed_len(string):
    matcher = re.compile(r'\(([0-9]+)x([0-9]+)\)').match

    decompressed_len = 0
    i = 0
    while i < len(string):
        m = matcher(string, i)
        if m:
            num_characters, repeat_times = map(int, m.groups())
            i = m.end(0)
            decompressed_len += repeat_times * len(string[i:i+num_characters])
            i += num_characters
        else:
            decompressed_len += 1
            i += 1
    return decompressed_len

def tests():
    assert decompress("ADVENT") == "ADVENT"
    assert decompress("A(1x5)BC") == "ABBBBBC"
    assert decompress("(3x3)XYZ") == "XYZXYZXYZ"
    assert decompress("A(2x2)BCD(2x2)EFG") == "ABCBCDEFEFG"
    assert decompress("(6x1)(1x3)A") == "(1x3)A"
    assert decompress("X(8x2)(3x3)ABCY") == "X(3x3)ABC(3x3)ABCY"

    assert decompressed_len_v2("(3x3)XYZ") == len("XYZXYZXYZ")
    assert decompressed_len_v2("X(8x2)(3x3)ABCY") == len("XABCABCABCABCABCABCY")
    assert decompressed_len_v2("(27x12)(20x12)(13x14)(7x10)(1x12)A") == 241920
    assert decompressed_len_v2("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN") == 445

    assert better_decompressed_len("ADVENT") == len("ADVENT")
    assert better_decompressed_len("A(1x5)BC") == len("ABBBBBC")
    assert better_decompressed_len("(3x3)XYZ") == len("XYZXYZXYZ")
    assert better_decompressed_len("A(2x2)BCD(2x2)EFG") == len("ABCBCDEFEFG")
    assert better_decompressed_len("(6x1)(1x3)A") == len("(1x3)A")
    assert better_decompressed_len("X(8x2)(3x3)ABCY") == len("X(3x3)ABC(3x3)ABCY")

tests()
part_one()
part_two()

