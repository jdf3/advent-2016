from itertools import permutations

def part_one():
    f = open("input.txt")
    text = f.read()

    string = "abcdefgh"
    print("Part one:", process(text, string))

def process(instructions, start):
    instructions = map(str.split, instructions.strip().split('\n'))
    string = list(start)

    for instr in instructions:
        if instr[0] == 'swap':
            p1 = 0
            p2 = 0
            if instr[1] == 'position':
                p1 = int(instr[2])
                p2 = int(instr[5])
            elif instr[1] == 'letter':
                p1 = string.index(instr[2])
                p2 = string.index(instr[5])
            string[p1], string[p2] = string[p2], string[p1]
        elif instr[0] == 'rotate':
            dir = 0
            steps = 0
            if instr[1] == 'left':
                dir = 1
                steps = int(instr[2])
            elif instr[1] == 'right':
                dir = -1
                steps = int(instr[2])
            elif instr[1] == 'based':
                index = string.index(instr[-1])
                steps = 1 + index
                if index >= 4:
                    steps += 1
                dir = -1
            new_string = []
            for i in range(len(string)):
                new_string.append(string[(i + dir * steps) % len(string)])
            string = new_string
        elif instr[0] == 'reverse':
            p1 = int(instr[2])
            p2 = int(instr[4])
            string[p1:p2+1] = string[p1:p2 + 1][::-1]
        elif instr[0] == 'move':
            p1 = int(instr[2])
            p2 = int(instr[5])
            c = string[p1]
            del string[p1]
            string.insert(p2,c)
    return ''.join(string)

def descramble(instructions, target):
    for combination in permutations(target):
        combination = ''.join(combination)
        if process(instructions, combination) == target:
            return combination

def part_two():
    f = open("input.txt")
    text = f.read().strip()

    target = "fbgdceah"
    print("Part two:", descramble(text, target))

def tests():
    assert process("""swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d""", "abcde") == "decab"

tests()
part_one()
part_two()
