import os
import json
import glob
import subprocess


def interpret(obj):
   pass
    
def interpretBytecode(byteArray, index = 0, stack = [], memory = []):
    byteObj = byteArray[index]
    print(str(index) + ": " +byteObj["opr"])
    match byteObj["opr"]:
        case "return":
            if byteObj["type"] is None:
                return None
            assert( len(stack) > 0)
            return stack.pop()

        case "push":
            stack.append( byteObj["value"]["value"] )

        case "load":
            print(byteObj)
            assert( len(memory) > byteObj["index"] )
            stack.append(memory[byteObj["index"]])

        case "binary":
            a = stack.pop()
            b = stack.pop()
            match byteObj["operant"]:
                case "add":
                    stack.append(a+b)
                case "mul":
                    stack.append(a*b)

        case "if":
            b = False
            match byteObj["condition"]:
                case "gt":
                    a = stack.pop()
                    b = stack.pop()
                    if b > a:
                        return interpretBytecode(byteArray, byteObj["target"], stack, memory)

        case "new":
            print(byteObj["opr"] + " not implemented")
            return
        case "dup":
            print(byteObj["opr"] + " not implemented")
            return 
        case "put":
            print(byteObj["opr"] + " not implemented")
            return
        case "invoke":
            print(byteObj["opr"] + " not implemented")
            return
        case "incr":
            print(byteObj["opr"] + " not implemented")
            return 
        case "ifz":
            print(byteObj["opr"] + " not implemented")
            return
        case "goto":
            print(byteObj["opr"] + " not implemented")
            return
        case _:
            print(byteObj["opr"] + " not implemented")
            return
    if(len(byteArray) > index):
        return interpretBytecode(byteArray, index+1, stack, memory)
    else :
        return "something"




def interpretProjDir(proj_directory: str):
    for file in glob.iglob(proj_directory + "/**/*.class", recursive=True):
        new_filename = "." + file.split('.')[1] + ".json"
        # ret = subprocess.run(["jvm2json", "-s", file, "-t", new_filename ])

        f = open( new_filename )
        data: json = json.load(f)
        f.close()
        interpret(data)

