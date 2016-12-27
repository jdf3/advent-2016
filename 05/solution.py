from hashlib import md5

door_id = "wtnhxymk"

def part_one():
    print("Simple method: ", get_password(door_id))

def get_password(door_id):
    password = ""
    i = 0
    while len(password) < 8:
        h = md5(bytes(door_id + str(i), "utf-8")).hexdigest()
        if h[:5] == "00000":
            #print("found ", i)
            password += h[5]
        i += 1
    return password

def part_two():
    print("Complicated method: ", get_more_complicated_password(door_id))

def get_more_complicated_password(door_id):
    password = [None, None, None, None, None, None, None, None]
    remaining = set(range(8))
    i = 0
    while len(remaining) > 0:
        h = md5(bytes(door_id + str(i), "utf-8")).hexdigest()
        if h[:5] == "00000":
            position = int(h[5], 16)
            if position in remaining:
                remaining.remove(position)
                password[position] = h[6]
                #print("filled position ", position, " with ", h[6])
        i += 1
    return ''.join(password)


def tests():
    assert get_password("abc") == "18f47a30"
    assert get_more_complicated_password("abc") == "05ace8e3"

tests()
part_one()
part_two()
