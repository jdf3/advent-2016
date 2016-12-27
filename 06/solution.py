def part_one():
    f = open("input.txt")
    data = f.read().strip()
    print("Max decode:", decode(data))

def part_two():
    f = open("input.txt")
    data = f.read().strip()
    print("Min decode:", decode(data, min_decode=True))

def decode(data, min_decode=False):
    lines = data.split('\n')
    length = len(lines[0])

    decoded_string = ""
    for j in range(length):
        frequencies = {}
        for i in range(len(lines)):
            if lines[i][j] in frequencies:
                frequencies[lines[i][j]] += 1
            else:
                frequencies[lines[i][j]] = 1
        if min_decode: char = min(frequencies.keys(), key=lambda k: frequencies[k])
        else: char = max(frequencies.keys(), key=lambda k: frequencies[k])
        decoded_string += char
    return decoded_string

def tests():
    assert decode("""eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar""") == "easter"
    assert decode("""eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar""", min_decode=True) == "advent"

tests()
part_one()
part_two()
