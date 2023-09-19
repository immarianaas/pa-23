import math
import os
import json
import glob
import interpreter

def testNoop():
    res = interpreter.interpretBytecode( [{ "offset": 0, "opr": "return", "type": None }])
    assert(res == None)
def testZero():
    res = interpreter.interpretBytecode( [
          {
            "offset": 0,
            "opr": "push",
            "value": { "type": "integer", "value": 0 }
          },
          { "offset": 1, "opr": "return", "type": "int" }
        ]
        )
    assert(res == 0)
    
def testHundredAndTwo():
    res = interpreter.interpretBytecode( [
          {
            "offset": 0,
            "opr": "push",
            "value": { "type": "integer", "value": 102 }
          },
          { "offset": 2, "opr": "return", "type": "int" }
        ]
        )
    assert(res == 102)

def testIdentity(a):
    res = interpreter.interpretBytecode(
        [
          { "offset": 0, "opr": "load", "type": "int", "index": 0 },
          { "offset": 1, "opr": "return", "type": "int" }
        ], memory={0:a}
    ) 
    assert(res == a)


def testAdd(a, b):
    res = interpreter.interpretBytecode( [
          { "offset": 0, "opr": "load", "type": "int", "index": 0 },
          { "offset": 1, "opr": "load", "type": "int", "index": 1 },
          { "offset": 2, "opr": "binary", "type": "int", "operant": "add" },
          { "offset": 3, "opr": "return", "type": "int" }
        ],memory={0: a, 1: b}
        )
    assert(res == a+b)
    
def testMin(a, b):
    res = interpreter.interpretBytecode([
          { "offset": 0, "opr": "load", "type": "int", "index": 0 },
          { "offset": 1, "opr": "load", "type": "int", "index": 1 },
          { "offset": 2, "opr": "if", "condition": "gt", "target": 5 },
          { "offset": 5, "opr": "load", "type": "int", "index": 0 },
          { "offset": 6, "opr": "return", "type": "int" },
          { "offset": 7, "opr": "load", "type": "int", "index": 1 },
          { "offset": 8, "opr": "return", "type": "int" }
        ], memory={0: a, 1: b})
    assert(res == min([a,b]))
    
def testFactorial(n):
    res = interpreter.interpretBytecode([
          { "offset": 0, "opr": "load", "type": "int", "index": 0 },
          { "offset": 1, "opr": "store", "type": "int", "index": 1 },
          { "offset": 2, "opr": "load", "type": "int", "index": 0 },
          { "offset": 3, "opr": "incr", "index": 0, "amount": -1 },
          { "offset": 6, "opr": "ifz", "condition": "le", "target": 10 },
          { "offset": 9, "opr": "load", "type": "int", "index": 1 },
          { "offset": 10, "opr": "load", "type": "int", "index": 0 },
          { "offset": 11, "opr": "binary", "type": "int", "operant": "mul" },
          { "offset": 12, "opr": "store", "type": "int", "index": 1 },
          { "offset": 13, "opr": "goto", "target": 2 },
          { "offset": 16, "opr": "load", "type": "int", "index": 1 },
          { "offset": 17, "opr": "return", "type": "int" }
        ], memory={0:n})
    assert(res == math.factorial(n))

testNoop()
testZero()
testHundredAndTwo()
testIdentity(5)
testAdd(40, 5)
testMin(3,4)
testFactorial(5)