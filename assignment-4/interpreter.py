import os
import json
import glob
import subprocess

def interpret(obj):
   pass
    
def interpretBytecode(byteArray, stack = [], memory = {}):
    byteObj = byteArray.pop(0)
    # print(byteObj)
    #print(stack)
    #print(byteObj, byteArray)
    match byteObj["opr"]:
        case "return":
            if byteObj["type"] is None:
                return None
            return stack.pop()

        case "push":
            stack.append( byteObj["value"]["value"] )
        case "load":
            pass
        case "new":
            pass
        case "dup":
            pass 
        case "put":
            pass
        case "invoke":
            pass
        case "binary":
            match byteObj["operant"]:
                case "add":
                    pass
    if(len(byteArray) > 0):
        return interpretBytecode(byteArray, stack, memory)
    else :
        return "something"

def testNoop():
    print(interpretBytecode( [{ "offset": 0, "opr": "return", "type": None }]))

def testZero():
    print(interpretBytecode( [
          {
            "offset": 0,
            "opr": "push",
            "value": { "type": "integer", "value": 0 }
          },
          { "offset": 1, "opr": "return", "type": "int" }
        ]
        ))
    
def testHundredAndTwo():
    print(interpretBytecode( [
          {
            "offset": 0,
            "opr": "push",
            "value": { "type": "integer", "value": 102 }
          },
          { "offset": 2, "opr": "return", "type": "int" }
        ]
        ))


def interpretProjDir(proj_directory: str):
    for file in glob.iglob(proj_directory + "/**/*.class", recursive=True):
        new_filename = "." + file.split('.')[1] + ".json"
        # ret = subprocess.run(["jvm2json", "-s", file, "-t", new_filename ])

        f = open( new_filename )
        data: json = json.load(f)
        f.close()
        interpret(data)



testNoop()
testZero()
testHundredAndTwo()