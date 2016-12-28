import re
from collections import defaultdict

def bots(instructions, goal=None):
    def give(giver, chip, recip):
        has[giver].discard(chip)
        has[recip].add(chip)
        chips = has[recip]
        if chips == goal:
            print(recip, 'has', goal)
        if len(chips) == 2:
            give(recip, min(chips), gives[recip][0])
            give(recip, max(chips), gives[recip][1])

    gives = {}
    for giver, low_dest, high_dest in re.findall(r'(bot \d+) gives low to (\w+ \d+) and high to (\w+ \d+)', instructions):
        gives[giver] = (low_dest, high_dest)

    has = defaultdict(set)
    for chip, recip in re.findall(r'value (\d+) goes to (\w+ \d+)', instructions):
        give('input bin', int(chip), recip)
    return has

def part_one():
    has = bots(open("input.txt").read(), goal={17, 61})

def part_two():
    has = bots(open("input.txt").read())
    print("Part two:",has['output 0'].pop() * has['output 1'].pop() * has['output 2'].pop())


def tests():
    instr = """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""
    has = bots(instr)
    assert has['output 0'] == set({5})
    assert has['output 1'] == set({2})
    assert has['output 2'] == set({3})

tests()
part_one()
part_two()
