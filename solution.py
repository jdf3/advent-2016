# not going for an efficient solution here, just a readable/maintainable one,
# since i don't know what's coming in part two

import re

def part_one():
    f = open("input.txt")
    data = f.read().split('\n')
    count = 0

    for line in data:
        if supports_abba(line): count += 1
    print("Part one:", count)

def supports_abba(ip):
    inside_pieces, outside_pieces = get_ip_pieces(ip)

    has_invalid_inside_piece = False
    for piece in inside_pieces:
        if contains_abba(piece):
            has_invalid_inside_piece = True
            break

    has_valid_outside_piece = False
    for piece in outside_pieces:
        if contains_abba(piece):
            has_valid_outside_piece = True
            break

    return has_valid_outside_piece and not has_invalid_inside_piece

def get_ip_pieces(ip):
    pattern = r"\[.+?\]"
    return (re.findall(pattern, ip), re.split(pattern, ip))

def contains_abba(piece):
    for i in range(len(piece) - 3):
        if piece[i] == piece[i + 3] and piece[i+1] == piece[i+2] and not piece[i] == piece[i+1]:
            return True
    return False

# WOW that turned out to be a lucky decision :)
def part_two():
    f = open("input.txt")
    data = f.read().split('\n')
    count = 0

    for line in data:
        if supports_ssl(line): count += 1
    print("Part two:", count)

# there are more efficient implementations, but i don't care right now. ;)
def supports_ssl(ip):
    inside_pieces, outside_pieces = get_ip_pieces(ip)

    inside_aba_set = set()
    for piece in inside_pieces:
        inside_aba_set = inside_aba_set.union(get_aba_set(piece))

    outside_aba_set = set()
    for piece in outside_pieces:
        outside_aba_set = outside_aba_set.union(get_aba_set(piece))

    outside_bab_set = set()
    for aba in outside_aba_set:
        outside_bab_set.add(''.join([aba[1], aba[0], aba[1]]))

    return len(inside_aba_set.intersection(outside_bab_set)) > 0

def get_aba_set(piece):
    aba_set = set()
    for i in range(len(piece) - 2):
        if piece[i] == piece[i+2] and piece[i] != piece[i+1]:
            aba_set.add(piece[i:i+3])
    return aba_set

def tests():
    assert contains_abba("aaaaaaaaaabbaaaaaaa")

    assert supports_abba("abba[mnop]qrst")
    assert not supports_abba("abcd[bddb]xyyx")
    assert not supports_abba("aaaa[qwer]tyui")
    assert supports_abba("ioxxoj[asdfgh]zxcvbn")

    assert supports_ssl("aba[bab]xyz")
    assert not supports_ssl("xyx[xyx]xyx")
    assert supports_ssl("aaa[kek]eke")
    assert supports_ssl("zazbz[bzb]cdb")

tests()
part_one()
part_two()
