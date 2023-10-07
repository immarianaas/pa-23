import os
import json
import glob
import subprocess
from collections import defaultdict

def interpretMethod(filepath, methodname):
    
    f = open("course-02242-examples/decompiled/eu/bogoe/dtu/exceptional/Arithmetics.json")
   
    obj = json.load(f)
    f.close()
    methods = obj["methods"]
    output = [i for i in methods if i["name"] == "alwaysThrows2"]
    m = output[0]
    return interpretBytecode(m["code"]["bytecode"])
   
    

    


def interpretBytecode(byteArray, index=0, stack=[], memory={}, exeptions = []):
    byteObj = byteArray[index]
    match byteObj["opr"]:   
        case "push":
            stack.append((byteObj["value"]["type"], [(byteObj["value"]["value"],byteObj["value"]["value"])])) 
        case "binary":
            (a_type, a_ranges) = stack.pop()
            (b_type, b_ranges) = stack.pop()
            match byteObj["operant"]:
                case "div":
                    if a_type != "integer":
                        exeptions.append((index, "UnsupportedOperationException"))
                    for i in a_ranges:
                        if (i[0] <= 0 <= i[1]):
                            exeptions.append((index, "ArithmeticException"))

                case _ : 
                    print(byteObj["operant"], " binary operation not implemented")
                    return
        case "store":
            memory[byteObj["index"]] = stack.pop()
        case "load":
            stack.append(memory[byteObj["index"]])
            

                    
        case _:
            print(byteObj["opr"] + " not implemented")
            return

    
    return interpretBytecode(byteArray, index+1, stack, memory, exeptions)



print(interpretMethod("course-02242-examples/decompiled/eu/bogoe/dtu/exceptional/Arithmetics.json", "alwaysThrows2"))