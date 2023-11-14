from abstraction import abstract_int, Enum, sign

# test ADD for signs - + 0 ? 
test_ADD = [
    (abstract_int(1), abstract_int(1), abstract_int(1)),
    (abstract_int(0), abstract_int(1), abstract_int(1)),

    (abstract_int(0), abstract_int(0), abstract_int(0)),

    (abstract_int(-1), abstract_int(-1), abstract_int(-1)),

    (abstract_int(1), abstract_int(-1), abstract_int()),
    (abstract_int(1), abstract_int(), abstract_int())
]

for x, y, expected_result in test_ADD:
    # print("Test ADD ", x, y, expected_result)
    assert str(x.add(y)) == str(expected_result)


# test MUL for signs - + 0 ? 
test_MUL = [
    (abstract_int(0), abstract_int(0), abstract_int(0)),
    (abstract_int(0), abstract_int(1), abstract_int(0)),
    (abstract_int(0), abstract_int(-1), abstract_int(0)),
    (abstract_int(0), abstract_int(), abstract_int(0)),

    (abstract_int(), abstract_int(-1), abstract_int()),
    (abstract_int(1), abstract_int(), abstract_int()),
    (abstract_int(), abstract_int(), abstract_int()),

    (abstract_int(-1), abstract_int(-1), abstract_int(1)),
    (abstract_int(1), abstract_int(1), abstract_int(1)),
    (abstract_int(1), abstract_int(1), abstract_int(1)),

    (abstract_int(1), abstract_int(-1), abstract_int(-1)),
    (abstract_int(-1), abstract_int(1), abstract_int(-1)),
]

for x, y, expected_result in test_MUL:
    # print("Test MUL" , x, y, expected_result)
    assert str(x.mul(y)) == str(expected_result)




# test SUB for signs - + 0 ? 
test_SUB = [
    (abstract_int(), abstract_int(-1), abstract_int()),
    (abstract_int(+1), abstract_int(), abstract_int()),
    (abstract_int(0), abstract_int(), abstract_int()),
    (abstract_int(), abstract_int(), abstract_int()),
    (abstract_int(-1), abstract_int(-1), abstract_int()),
    (abstract_int(1), abstract_int(1), abstract_int()),

    (abstract_int(0), abstract_int(0), abstract_int(0)),

    (abstract_int(0), abstract_int(-1), abstract_int(1)),
    (abstract_int(1), abstract_int(0), abstract_int(1)),
    (abstract_int(1), abstract_int(-1), abstract_int(1)),

    (abstract_int(-1), abstract_int(0), abstract_int(-1)),
    (abstract_int(0), abstract_int(1), abstract_int(-1)),
    (abstract_int(-1), abstract_int(1), abstract_int(-1)),
]

for x, y, expected_result in test_SUB:
    # print("Test MUL" , x, y, expected_result)
    assert str(x.sub(y)) == str(expected_result)