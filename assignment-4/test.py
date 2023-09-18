import os
import json
import glob
import interpreter

def testNoop():
    print(interpreter.interpretBytecode( [{ "offset": 0, "opr": "return", "type": None }]))

def testZero():
    print(interpreter.interpretBytecode( [
          {
            "offset": 0,
            "opr": "push",
            "value": { "type": "integer", "value": 0 }
          },
          { "offset": 1, "opr": "return", "type": "int" }
        ]
        ))
    
def testHundredAndTwo():
    print(interpreter.interpretBytecode( [
          {
            "offset": 0,
            "opr": "push",
            "value": { "type": "integer", "value": 102 }
          },
          { "offset": 2, "opr": "return", "type": "int" }
        ]
        ))

def testIdentity(a):
    print(interpreter.interpretBytecode(
        [
          { "offset": 0, "opr": "load", "type": "int", "index": 0 },
          { "offset": 1, "opr": "return", "type": "int" }
        ], memory=[a]
    ) )


def testAdd(a, b):
    print(interpreter.interpretBytecode( [
          { "offset": 0, "opr": "load", "type": "int", "index": 0 },
          { "offset": 1, "opr": "load", "type": "int", "index": 1 },
          { "offset": 2, "opr": "binary", "type": "int", "operant": "add" },
          { "offset": 3, "opr": "return", "type": "int" }
        ],memory= [a, b]
        ))

testNoop()
testZero()
testHundredAndTwo()

testAdd(40, 5)

testHundredAndTwo()

testIdentity(5)
