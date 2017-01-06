from collections import defaultdict
from itertools import islice
from itertools import cycle

def process(text, a_initial_value=0):
    instructions = list(map(lambda line: line.split(' '), text.strip().split('\n')))
    variables = defaultdict(int)
    variables['a'] = a_initial_value
    letters = frozenset({'a', 'b', 'c', 'd', 'e', 'f'})
    i = 0
    furthest = 0
    while i < len(instructions):
        #if i > furthest: print(furthest); furthest = i
        instruction = instructions[i]
        name = instruction[0]
        i += 1
        if name == "cpy":
            if not instruction[2] in letters: continue
            f = instruction[1]
            to_assign = int(variables[f]) if f in letters else int(f)
            variables[instruction[2]] = to_assign
        elif name == "inc":
            variables[instruction[1]] += 1
        elif name == "dec":
            variables[instruction[1]] -= 1
        elif name == "tgl":
            f = instruction[1]
            to_toggle = i - 1 + int(variables[f]) if f in letters else int(f)
            if to_toggle >= len(instructions): continue
            pointed_instruction = instructions[to_toggle]
            if len(pointed_instruction) == 3:
                if pointed_instruction[0] == "jnz":
                    pointed_instruction[0] = "cpy"
                else:
                    pointed_instruction[0] = "jnz"
            elif len(pointed_instruction) == 2:
                if pointed_instruction[0] == "inc":
                    pointed_instruction[0] = "dec"
                else:
                    pointed_instruction[0] = "inc"
            instructions[to_toggle] = pointed_instruction
        elif name == "jnz":
            f = instruction[1]
            value = int(variables[f]) if f in letters else int(f)
            if value != 0:
                i -= 1
                to_jump = instruction[2]
                to_jump = int(variables[to_jump] if to_jump in letters else int(to_jump))
                i += to_jump
        elif name == "out":
            f = instruction[1]
            value = int(variables[f]) if f in letters else int(f)
            yield value


def part_one():
    f = open("input.txt")
    text = f.read().strip()

    a = find_infinite(text)
    print("Part one:", a)

def find_infinite(text):
    a = 0
    while True:
        a += 1
        signals = process(text, a_initial_value=a)
        i = 0
        for _, (actual, expected) in enumerate(zip(signals, cycle((0, 1)))):
            if actual != expected:
                found = False
                break
            i += 1
            if i > 100:
                return a

part_one()
