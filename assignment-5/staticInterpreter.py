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
    output = [i for i in methods if i["name"] == "alwaysThrows1"]
    m = output[0]
    return interpretBytecode(m["code"]["bytecode"])
   
    

    


def interpretBytecode(byteArray, index=0, stack=[], memory={}):
    byteObj = byteArray[index]
    match byteObj["opr"]:   
        case "push":
            stack.append((byteObj["value"]["type"], [0])) 
        case "binary":
            (a_type, a_ranges) = stack.pop()
            (b_type, b_ranges) = stack.pop()
            match byteObj["operant"]:
                case "div":
                    if a_type != "integer":
                        return "UnsupportedOperationException"
                    for i in a_ranges:
                        if i == 0:
                            return "ArithmeticException"
                        if isinstance(i, tuple) & (i[0] <= 0 <= i[1]):
                            return "ArithmeticException"
                case _ : 
                    print(byteObj["operant"], "not implemented")
                    return

                    
        case _:
            print(byteObj["opr"] + " not implemented")
            return

    
    return interpretBytecode(byteArray, index+1, stack, memory)



print(interpretMethod("course-02242-examples/decompiled/eu/bogoe/dtu/exceptional/Arithmetics.json", "alwaysThrows2"))