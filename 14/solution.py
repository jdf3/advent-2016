import re

from hashlib import md5
from itertools import islice
from collections import defaultdict

def md5_digest(string):
    return md5(bytes(string, 'utf-8')).hexdigest()

def get_keys(salt, h_func=md5_digest):
    fives = defaultdict(frozenset)
    hashes = defaultdict(str)
    for i in range(1000):
        hashes[i] = h_func(salt + str(i))
        fives[i] = frozenset(re.findall(r'(.)\1{4}', hashes[i]))

    i = -1
    while True:
        i += 1
        hashed = hashes[i]
        match = re.search(r'(.)\1{2}', hashed)
        hashes[i + 1000] = h_func(salt + str(i + 1000))
        fives[i + 1000] = frozenset(re.findall(r'(.)\1{4}', hashes[i + 1000]))
        if match:
            triple = match.group(0)
            for i2 in range(i + 1, i + 1000):
                if triple[0] in fives[i2]:
                    #print(i, i2, triple[0])
                    yield i
                    break

def hash_2016(string):
    h = string
    for i in range(2017):
        h = md5(bytes(h, 'utf-8')).hexdigest()
    return h

def tests():
    assert next(islice(get_keys('abc'), 63, 64)) == 22728
    assert next(islice(get_keys('abc', h_func=hash_2016), 63, 64)) == 22551

#tests()

def part_one():
    print("Part one:", next(islice(get_keys('qzyelonm'), 63, 64)))

part_one()

def part_two():
    print("Part two:", next(islice(get_keys('qzyelonm', h_func=hash_2016), 63, 64)))

part_two()


