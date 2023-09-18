import os
import json
import glob
import subprocess


def interpret(obj):
   pass
    
def interpretBytecode(byteArray, stack = [], memory = []):
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
            stack.append(memory[byteObj["index"]])
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
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a+b)
    if(len(byteArray) > 0):
        return interpretBytecode(byteArray, stack, memory)
    else :
        return "something"


def testAdd():
    print(interpretBytecode( [
          { "offset": 0, "opr": "load", "type": "int", "index": 0 },
          { "offset": 1, "opr": "load", "type": "int", "index": 1 },
          { "offset": 2, "opr": "binary", "type": "int", "operant": "add" },
          { "offset": 3, "opr": "return", "type": "int" }
        ],memory= [10, 11]
        ))

def testAdd():
    print(interpretBytecode( [
          { "offset": 0, "opr": "load", "type": "int", "index": 0 },
          { "offset": 1, "opr": "load", "type": "int", "index": 1 },
          { "offset": 2, "opr": "binary", "type": "int", "operant": "add" },
          { "offset": 3, "opr": "return", "type": "int" }
        ],memory= [10, 11]
        ))


def interpretProjDir(proj_directory: str):
    for file in glob.iglob(proj_directory + "/**/*.class", recursive=True):
        new_filename = "." + file.split('.')[1] + ".json"
        # ret = subprocess.run(["jvm2json", "-s", file, "-t", new_filename ])

        f = open( new_filename )
        data: json = json.load(f)
        f.close()
        interpret(data)


testAdd()