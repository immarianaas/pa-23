import os
import json
import glob
import subprocess
from collections import defaultdict


def interpretBytecode(byteArray, index=0, stack=[], memory={}):
    byteObj = byteArray[index]
    # print(byteObj, '\n')
    match byteObj["opr"]:   
        case "push":
            stack.append(byteObj["value"]) 
        case "binary":
            a = stack.pop()
            b = stack.pop()
            print(a)
            match byteObj["operant"]:
                case "div":
                    if a["value"] == 0:
                        return "Trows 1"

                    
        case _:
            print(byteObj["opr"] + " not implemented")
            return

    # print(byteArray)
    if (len(byteArray) > index):
        return interpretBytecode(byteArray, index+1, stack, memory)
    else:
        return "something"


