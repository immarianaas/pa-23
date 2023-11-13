from abstraction import abstract_int, Enum, sign

x = abstract_int(1)
y = abstract_int(1)
assert(str(x.add(y)) == str(abstract_int(1)))

x = abstract_int(0)
y = abstract_int(1)
assert(str(x.add(y)) == str(abstract_int(1)))

x = abstract_int(1)
y = abstract_int(0)
assert(str(x.add(y)) == str(abstract_int(1)))

x = abstract_int(1)
y = abstract_int(-1)
assert(str(x.add(y)) == str(abstract_int()))