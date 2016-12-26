def parse_one(instructions, keypad, starting_position):
    position = starting_position
    for char in instructions:
        if char == 'U' and keypad[position[0] - 1][position[1]] != '.':
            position[0] = position[0] - 1
        if char == 'L' and keypad[position[0]][position[1] - 1] != '.':
            position[1] = position[1] - 1
        if char == 'D' and keypad[position[0] + 1][position[1]] != '.':
            position[0] = position[0] + 1
        if char == 'R' and keypad[position[0]][position[1] + 1] != '.':
            position[1] = position[1] + 1
    return keypad[position[0]][position[1]]

def tests():
    str_pad = """
    .....
    .123.
    .456.
    .789.
    .....
    """

    Keypad = str.split
    keypad = Keypad(str_pad)

    assert int(parse_one("DDDDDDDUDUDUDUDUDUDU", keypad, [2, 2])) == 5

def parse_multiple(instructions, keypad, starting_position):
    code = ""
    for line in instructions:
        code += parse_one(line, keypad, starting_position)
    return code

def part_one():
    f = open("input.txt")
    text = f.read()

    str_pad = """
    .....
    .123.
    .456.
    .789.
    .....
    """

    keypad = str.split(str_pad)

    instructions = str.split(text)
    starting_position = [2, 2]
    print(parse_multiple(instructions, keypad, starting_position))

def part_two():
    f = open("input2.txt")
    text = f.read()

    str_pad = """
    .......
    ...1...
    ..234..
    .56789.
    ..ABC..
    ...D...
    .......
    """

    starting_position = [3, 1]

    keypad = str.split(str_pad)

    instructions = str.split(text)
    print(parse_multiple(instructions, keypad, starting_position))

tests()
part_one()
part_two()
