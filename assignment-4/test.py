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
    

testNoop()
testZero()
testHundredAndTwo()