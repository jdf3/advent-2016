from collections import defaultdict

def process(text, initial_value=0):
    instructions = list(map(lambda line: line.split(' '), text.strip().split('\n')))
    variables = defaultdict(int)
    variables['a'] = initial_value
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
    return variables


def tests():
    instructions = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""
    assert process(instructions)['a'] == 42
    instructions = """cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a"""
    assert process(instructions)['a'] == 3

#def pretty_print(instructions):
#    for instruction in instructions:
#        print(*instruction)

tests()

def part_one():
    f = open("input.txt")
    text = f.read()
    print("Part one:", process(text, initial_value=7)['a'])

def part_two():
    f = open("input.txt")
    text = f.read()
    print("Part one:", process(text, initial_value=12)['a'])

part_one()
part_two()
