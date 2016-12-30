def get_data(initial, size):
    s = initial
    while len(s) < size:
        a = s
        b = []
        for c in a[::-1]:
            if c == '0':
                b.append('1')
            else:
                b.append('0')
        s = a + "0" + ''.join(b)
    return s[:size]

def get_checksum(initial, size):
    s = get_data(initial, size)
    chk = s
    while len(chk) % 2 == 0:
        chk2 = []
        for i in range(0, len(chk), 2):
            chk2.append('1' if chk[i] == chk[i+1] else '0')
        chk = chk2
    return ''.join(chk)

def tests():
    assert get_data("0", 3) == "001"
    assert get_data("1", 3) == "100"
    assert get_data("11111", 11) == "11111000000"
    assert get_data("111100001010", 20) == "11110000101001010111"
    assert get_checksum("10000", 20) == "01100"

def part_one():
    print("Part one:", get_checksum("10010000000110000", 272))

def part_two():
    print("Part two:", get_checksum("10010000000110000", 35651584))

tests()
part_one()
part_two()
