import re
from functools import cmp_to_key

def part_one():
    f = open("input.txt")
    text = f.read().strip()
    room_triples = parse_input(text)
    s = 0
    for name, sector, checksum in room_triples:
        if is_valid_room(name, checksum):
            s += int(sector)
    print("Sum of valid sector IDs: {0}".format(s))

def parse_input(text):
    lines = text.split('\n')
    return list(map(parse_one, lines))

# returns a triple
def parse_one(line):
    return re.match(r"(.+)-(.+?)\[([a-z]+)\]", line).groups()

def get_text_from_file(filename):
    f = open(filename)
    return f.read()

def parse_tests():
    assert parse_one("aaaaa-bbb-z-y-x-123[abxyz]") == ("aaaaa-bbb-z-y-x", "123", "abxyz")
    assert parse_input("aaaaa-bbb-z-y-x-123[abxyz]\na-b-c-d-e-f-g-h-987[abcde]") == [("aaaaa-bbb-z-y-x", "123", "abxyz"), ("a-b-c-d-e-f-g-h", "987", "abcde")]

def is_valid_room(name, checksum):
    correct_checksum = get_checksum(name)
    return checksum == correct_checksum

def make_comparator(d):
    def compare(x, y):
        if d[x] > d[y]:
            return -1
        if d[x] < d[y]:
            return 1
        if x < y:
            return -1
        if x > y:
            return 1
        return 0
    return compare

def get_checksum(name):
    freq = {}
    for char in name:
        if char != '-':
            if char in freq: freq[char] += 1
            else: freq[char] = 1
    comparator = make_comparator(freq)
    sorted_frequencies = sorted(freq, key=cmp_to_key(comparator))
    return ''.join(sorted_frequencies[:5])


def valid_tests():
    assert is_valid_room("aaaaa-bbb-z-y-x", "abxyz")
    assert is_valid_room("a-b-c-d-e-f-g-h", "abcde")
    assert is_valid_room("not-a-real-room", "oarel")
    assert not is_valid_room("totally-real-room", "decoy")

def part_two():
    f = open("input.txt")
    text = f.read().strip()
    room_triples = parse_input(text)
    for name, sector, checksum in room_triples:
        if is_valid_room(name, checksum):
            decrypted_name = decrypt_name(name, int(sector))
            if "north" in decrypted_name: print("{0}: {1}".format(decrypted_name, sector))

def decrypt_name(name, sector):
    modulus = sector % 26
    decrypted_name = []
    for c in name:
        if c == '-':
            decrypted_name.append(' ')
            continue
        dec_chr = chr(((ord(c) - ord('a') + sector) % 26) + ord('a'))
        decrypted_name.append(dec_chr)
    return ''.join(decrypted_name)

def decrypt_tests():
    assert decrypt_name("qzmt-zixmtkozy-ivhz", 343) == "very encrypted name"

def tests():
    parse_tests()
    valid_tests()
    decrypt_tests()

tests()

part_one()

part_two()
