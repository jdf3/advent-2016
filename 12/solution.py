from collections import defaultdict

def process(text):
    instructions = list(map(lambda line: line.split(' '), text.strip().split('\n')))
    variables = defaultdict(int)
    letters = frozenset({'a', 'b', 'c', 'd', 'e', 'f'})
    i = 0
    while i < len(instructions):
        instruction = instructions[i]
        name = instruction[0]
        i += 1
        if name == "cpy":
            f = instruction[1]
            to_assign = int(variables[f]) if f in letters else int(f)
            variables[instruction[2]] = to_assign
        elif name == "inc":
            variables[instruction[1]] += 1
        elif name == "dec":
            variables[instruction[1]] -= 1
        else:
            f = instruction[1]
            value = int(variables[f]) if f in letters else int(f)
            if value != 0:
                i -= 1
                i += int(instruction[2])
    return variables


def tests():
    instructions = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""
    assert process(instructions)['a'] == 42

tests()

def part_one():
    f = open("input.txt")
    instructions = f.read()
    print("Part one:", process(instructions)['a'])

part_one()

def part_two():
    f = open("input.txt")
    instructions = "cpy 1 c\n" + f.read()
    print("Part two:", process(instructions)['a'])

part_two()
