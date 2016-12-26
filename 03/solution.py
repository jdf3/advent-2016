def part_one():
    f = open("input.txt")
    triangle_tuples = list(map(lambda line: list(map(int, line.split())), f.read().split('\n')))
    valid_tuples = (item for item in triangle_tuples if is_valid_triangle(item))
    print(len(list(valid_tuples)))

def is_valid_triangle(triple):
    if len(triple) != 3: return False
    t = sorted(triple)
    return t[0] + t[1] > t[2]

def part_two():
    f = open("input.txt")
    tuples = list(map(lambda line: list(map(int, line.split())), f.read().split('\n')))
    count = 0
    for j in range(3):
        for i in range(0, len(tuples) - 2, 3):
            print(i, j)
            if is_valid_triangle((tuples[i][j], tuples[i+1][j], tuples[i+2][j])):
                count += 1
    print(count)


def tests():
    assert is_valid_triangle([2, 5, 9]) == False
    assert is_valid_triangle([2, 5, 4]) == True

tests()
part_one()
part_two()
