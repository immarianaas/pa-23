import math
import os
import json
import glob
import interpreter


def testNoop():
    res = interpreter.interpretBytecode(
        [{"offset": 0, "opr": "return", "type": None}])
    assert (res == None)


def testZero():
    res = interpreter.interpretBytecode([
        {
            "offset": 0,
            "opr": "push",
            "value": {"type": "integer", "value": 0}
        },
        {"offset": 1, "opr": "return", "type": "int"}
    ]
    )
    assert (res == 0)


def testHundredAndTwo():
    res = interpreter.interpretBytecode([
        {
            "offset": 0,
            "opr": "push",
            "value": {"type": "integer", "value": 102}
        },
        {"offset": 2, "opr": "return", "type": "int"}
    ]
    )
    assert (res == 102)


def testIdentity(a):
    res = interpreter.interpretBytecode(
        [
            {"offset": 0, "opr": "load", "type": "int", "index": 0},
            {"offset": 1, "opr": "return", "type": "int"}
        ], memory={0: a}
    )
    assert (res == a)


def testAdd(a, b):
    res = interpreter.interpretBytecode([
        {"offset": 0, "opr": "load", "type": "int", "index": 0},
        {"offset": 1, "opr": "load", "type": "int", "index": 1},
        {"offset": 2, "opr": "binary", "type": "int", "operant": "add"},
        {"offset": 3, "opr": "return", "type": "int"}
    ], memory={0: a, 1: b}
    )
    assert (res == a+b)


def testMin(a, b):
    res = interpreter.interpretBytecode([
        {"offset": 0, "opr": "load", "type": "int", "index": 0},
        {"offset": 1, "opr": "load", "type": "int", "index": 1},
        {"offset": 2, "opr": "if", "condition": "gt", "target": 5},
        {"offset": 5, "opr": "load", "type": "int", "index": 0},
        {"offset": 6, "opr": "return", "type": "int"},
        {"offset": 7, "opr": "load", "type": "int", "index": 1},
        {"offset": 8, "opr": "return", "type": "int"}
    ], memory={0: a, 1: b})
    assert (res == min([a, b]))


def testFactorial(n):
    res = interpreter.interpretBytecode([
        {"offset": 0, "opr": "load", "type": "int", "index": 0},
        {"offset": 1, "opr": "store", "type": "int", "index": 1},
        {"offset": 2, "opr": "load", "type": "int", "index": 0},
        {"offset": 3, "opr": "incr", "index": 0, "amount": -1},
        {"offset": 6, "opr": "ifz", "condition": "le", "target": 10},
        {"offset": 9, "opr": "load", "type": "int", "index": 1},
        {"offset": 10, "opr": "load", "type": "int", "index": 0},
        {"offset": 11, "opr": "binary", "type": "int", "operant": "mul"},
        {"offset": 12, "opr": "store", "type": "int", "index": 1},
        {"offset": 13, "opr": "goto", "target": 2},
        {"offset": 16, "opr": "load", "type": "int", "index": 1},
        {"offset": 17, "opr": "return", "type": "int"}
    ], memory={0: n})
    assert (res == math.factorial(n))



# def testFib(n):
#     def f(n): return 1 if n <= 2 else f(n-1) + f(n-2)
#     print(f(10))
#     res = interpreter.interpretBytecode([
#         {"offset": 0, "opr": "load", "type": "int", "index": 0},
#         {"offset": 1,   "opr": "push", "value":
#          {"type": "integer", "value": 2}},
#         {"offset": 2, "opr": "if", "condition": "ge", "target": 5},
#         {"offset": 5, "opr": "push", "value":
#          {"type": "integer",    "value": 1}},
#         {"offset": 6, "opr": "return", "type": "int"},
#         {"offset": 7, "opr": "load", "type": "int", "index": 0},
#         {"offset": 8, "opr": "push", "value":
#          {"type": "integer",    "value": 1}},
#         {"offset": 9, "opr": "binary", "type": "int", "operant": "sub"},
#         {"offset": 10, "opr": "invoke", "access": "static", "method":
#          {"is_interface": False, "ref":
#           {"kind": "class", "name": "dtu/compute/exec/Calls"},
#           "name": "fib",    "args": ["int"],    "returns": "int"}},
#         {"offset": 13, "opr": "load", "type": "int", "index": 0},
#         {"offset": 14, "opr": "push", "value":
#          {"type": "integer",    "value": 2}},
#         {"offset": 15, "opr": "binary", "type": "int", "operant": "sub"},
#         {"offset": 16, "opr": "invoke", "access": "static", "method":
#          {"is_interface": False,    "ref":
#           {"kind": "class",        "name": "dtu/compute/exec/Calls"},    "name": "fib",    "args": ["int"],    "returns": "int"}},
#         {"offset": 19, "opr": "binary", "type": "int", "operant": "mul"},
#         {"offset": 20, "opr": "return", "type": "int"}
#     ], memory={0: n})
#     print(res)
#     assert (res == f(n))

def testArrayFirst(n):
    res = interpreter.interpretBytecode([
        {"offset": 0,"opr": "load","type": "ref","index": 0},
        {"offset": 1,"opr": "push","value": {"type": "integer","value": 0}},
        {"offset": 2,"opr": "array_load","type": "int"},
        {"offset": 3,"opr": "return","type": "int"}
        ], memory={0:n})
    assert (res == n[0])

def testArrayAccess(i, n):
    res = interpreter.interpretBytecode([
        {"offset": 0,"opr": "load","type": "ref","index": 1}, 
        {"offset": 1,"opr": "load","type": "int","index": 0}, 
        {"offset": 2,"opr": "array_load","type": "int"}, 
        {"offset": 3,"opr": "return","type": "int"}
        ], memory={0:i, 1:n})
    assert (res == 5)


testNoop()
testZero()
testHundredAndTwo()
testIdentity(5)
testAdd(40, 5)
testMin(3, 4)
testFactorial(5)

# testFib(5)
testArrayFirst([5,7])
testArrayAccess(0,[5,7])
# ugly but just for testing!!!
# calls_obj = interpreter.interpretProjDir(os.path.join("..", "assignment-3", "classes"))

# a = interpreter.interpret(calls_obj, "fib", memory={0: 5})
# print(a)
