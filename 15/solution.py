"""
Disc #1 has 17 positions; at time=0, it is at position 1.
Disc #2 has 7 positions; at time=0, it is at position 0.
Disc #3 has 19 positions; at time=0, it is at position 2.
Disc #4 has 5 positions; at time=0, it is at position 0.
Disc #5 has 3 positions; at time=0, it is at position 0.
Disc #6 has 13 positions; at time=0, it is at position 5.

#n requires time=(positions) - (n) - (current position)
#1 requires time=17 - 1 - 1 mod 17  (15 mod 17)
#2 requires time=7 - 2 mod 7        (5 mod 7)
#3 requires time=19 - 3 - 2 mod 19  (14 mod 19)
#4 requires time=5 - 4 - 0 mod 5    (1 mod 5)
#5 requires time=3 - 5 - 0 mod 3    (1 mod 3)
#6 requires time=13 - 6 - 5 mod 13  (2 mod 13)

17, 7, 19, 5, 3, and 13 are all relatively prime! So actually, there's only one
solution below their product... but it doesn't matter. Our solution can build
them up from "the ground floor" anyway.

The steps would look something like this: we know our solution has to look
like:

15 + (x * 17)

So if we want this to satisfy 5 mod 7, we need to keep incrementing x (in range
0-6) until we satisfy this. These numbers are all prime, so they're also
coprime, so there's a unique solution. In this case, x = 5 works.

So we'd continue on, looking at 117 + (x * 119), incrementing x in 0-18 until
we satisfy it's equivalent to 14 modulo 19.

I don't believe there's a fancy (non-imperative) way to calculate the
appropriate number without some computation, but I'd really like to know if
there is...

"""

import re

# instructions are iterable of 3-tuple of ints: disc, positions, and
# current position
def process(instructions):
    n, m = 0, 1
    #n, m = 15, 17
    for index, positions, cur_pos in instructions:
        n2, m2 = positions - index - cur_pos % positions, positions
        if (n2 < 0): n2 += m2
        if n % m2 != n2:
            for i in range(positions):
                n += m
                if n % m2 == n2:
                    break
        # assumes co-prime, else would need lcm/gcd, and could shorten
        # "range(positions)"
        m *= positions
    return n

def tests():
    assert process([(1, 5, 4), (2, 2, 1)]) == 5

def part_one():
    f = open("input.txt")
    text = f.read().strip()
    instructions = list(map(lambda match: tuple(map(int, match)),
        re.findall(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).', text)))
    print("Part one:", process(instructions))

def part_two():
    f = open("input.txt")
    text = f.read().strip()
    instructions = list(map(lambda match: tuple(map(int, match)),
        re.findall(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).', text)))
    instructions.append((7, 11, 0))
    print("Part two:", process(instructions))

tests()
part_one()
part_two()
