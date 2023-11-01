import copy
import json
import math
import os
from pathlib import Path
import random
import numpy


intTypes = ["int", "integer"]
primitiveTypes = ["byte", "short", "int", "integer", "long", "float", "double", "boolean" ,"char"]


def InterpretFunction(
    dir: str, file: str, function: str = "main", clas: str = None, stack=[], memory={}, printDebug =False
) -> (any, set):
    try:
        f = open(dir + "/" + file + ".json", "r")
        f.close
    except:
        print(dir + "/" + file + ".json" + " not found")
        return None
    obj = json.load(f)
    methods = obj["methods"]
    fun = [f for f in methods if f["name"] == function][0]
    byteArray = fun["code"]["bytecode"]
    if printDebug: print("\n------------ Interpreting ", fun["name"], " -----------------")
    return interpretBytecode(
        byteArray=byteArray,
        function=obj["name"] + "/" + fun["name"],
        dir=dir,
        memory=memory,
        stack=stack,
        printDebug = printDebug
    )

def error(): 
    print("There was an Error")
    return

def newIndexRef(memory):
    keys = list(memory.keys())
    keys.sort()
    if len(keys)>0:
        return keys[0]-1
    return -1

def getStaticField(dir, field):

    try:
        f = open(dir + "/" + field["class"] + ".json", "r")
        f.close
        obj = json.load(f)
        fields = obj["fields"]
        val = [f for f in fields if f["name"] == field["name"]][0]
        return val
    except:
        print(dir + "/" + field["class"] + ".json" + " not found")
        return #{"value": random.randrange(9999), "type": "ref"}
    
    obj = json.load(f)
    fields = obj["fields"]
    field = [f for f in fields if f["name"] == field["name"]][0]
    return field
    
def interpretBytecode(
    byteArray: [], function: str, dir, stack: [], memory: dict, index: int = 0, printDebug = False,
):
    byteObj = byteArray[index]
    if printDebug: print("\n    -- ", stack, "\n    -- ", memory, "\n\n", index ,":" ,byteObj  )
    index = index + 1
    match byteObj["opr"]:
        case "arraylength":
            ref = stack.pop()
            stack.append(memory[ref["value"]]["value"]["len"])
        case "array_load":
            i = stack.pop()["value"]
            ref = stack.pop()
            a = memory[ref["value"]]["value"]["content"]
            stack.append(a[i])
        case "array_store":
            v = stack.pop()
            i = stack.pop()
            ref = stack.pop()
            memory[ref["value"]]["value"]["content"][i["value"]]= v
        case "binary":
            v2 = stack.pop()
            v1 = stack.pop()
            assert v1["type"] == v2["type"]
            match byteObj["operant"]:
                case "add":
                    stack.append(
                        {"value": v1["value"] + v2["value"], "type": v1["type"]}
                    )
                case "sub":
                    stack.append(
                        {"value": v1["value"] - v2["value"], "type": v1["type"]}
                    )
                case "div":
                    stack.append(
                        {"value": v1["value"] / v2["value"], "type": v1["type"]}
                    )
                case "mul":
                    stack.append(
                        {"value": v1["value"] * v2["value"], "type": v1["type"]}
                    )
                case "rem":
                    stack.append(
                        {"value": math.remainder(v1["value"] , v2["value"]), "type": v1["type"]}
                    )
                case _:
                    error()
        case "dup":
            vals = stack[-byteObj["words"] :]
            stack = stack[: len(stack) - byteObj["words"]]
            for v in vals:
                stack.append(v)
                stack.append(v)
        case "get":
            if(byteObj["static"] == True):
                value = getStaticField(dir=dir,field = byteObj["field"] )
                stack.append(value)
            else:
                print("get not implemented")
        case "goto":
            index = byteObj["target"]
        case "if":
            v2 = stack.pop()
            v1 = stack.pop()
            assert v1["type"] in intTypes and v2["type"] in intTypes
            match byteObj["condition"]:
                case "eq":
                    if v1["value"] == v2["value"]:
                        index = byteObj["target"]
                case "ne":
                    if v1["value"] != v2["value"]:
                        index = byteObj["target"]
                case "gt":
                    if v1["value"] > v2["value"]:
                        index = byteObj["target"]
                case "ge":
                    if v1["value"] >= v2["value"]:
                        index = byteObj["target"]
                case "lt":
                    if v1["value"] < v2["value"]:
                        index = byteObj["target"]
                case "le":
                    if v1["value"] <= v2["value"]:
                        index = byteObj["target"]
                case _:
                    error()
        case "ifz":
            v = stack.pop()
            if v["type"] in intTypes:
                match byteObj["condition"]:
                    case "eq":
                        if v["value"] == 0:
                            index = byteObj["target"]
                    case "ne":
                        if v["value"] != 0:
                            index = byteObj["target"]
                    case "gt":
                        if v["value"] > 0:
                            index = byteObj["target"]
                    case "ge":
                        if v["value"] >= 0:
                            index = byteObj["target"]
                    case "lt":
                        if v["value"] < 0:
                            index = byteObj["target"]
                    case "le":
                        if v["value"] <= 0:
                            index = byteObj["target"]
                    case _:
                        error()
            else:
                match byteObj["condition"]:
                    case "ne":
                        if v["value"] != None:
                            index = byteObj["target"]
                    case "eq":
                        if v["value"] == None:
                            index = byteObj["target"]
                    case _:
                        error()
            
        case "incr":
            v = memory[byteObj["index"]]["value"]
            memory[byteObj["index"]]["value"]  = v+byteObj["amount"]
        case "invoke":
            method = byteObj["method"]
            num_args = len(method["args"])
            mem = {i: v for i, v in enumerate(stack[-num_args:])}
            stack = stack[: (len(stack) - num_args)]
            if byteObj["access"] == "static" and not method["is_interface"]:
                res = InterpretFunction(
                    dir=dir,
                    file=method["ref"]["name"],
                    function=method["name"],
                    stack=[],
                    memory=mem,
                    printDebug=printDebug
                )
                stack.append(res)
            else:
                print("Invoke not implementet for case", byteObj)

        case "load":
            stack.append(copy.deepcopy(memory[byteObj["index"]]))

        case "newarray":
            ref = newRef()
            i = stack.pop()["value"]
            array = {index: {"type": None, "value": None} for index in range(i)}
            memory[ref] = {"value":{ "content": array, "len": {'type': 'integer', 'value': i}}, "type": "integer array"}
            stack.append({"value": ref, "type": "ref"})
        case "push":
            stack.append(byteObj["value"])
        case "return":
            if byteObj["type"] == None :
                return {'type': None, 'value': None}
            else:
                res = stack.pop()
                # assert res["type"] == byteObj["type"]
                return res
        case "store":
            memory[byteObj["index"]] = stack.pop()
            
        case "throw":
            raise RuntimeError("Throwing an exception (incomplete)")
        case _:
            print(byteObj["opr"] + " not implemented in" + function)
            print(byteObj)
            return

    

    if len(byteArray) > index:
        return interpretBytecode(
            byteArray,
            dir=dir,
            function=function,
            index=index,
            stack=stack,
            memory=memory,
            printDebug = printDebug
        )
    else:
        return "Error - index out of range"

def newRef():
    return random.randrange(1000, 9999)


""" 
        case "get":
            if byteObj["static"] == True:
                stack.append(
                    byteObj["field"]["type"]["name"] + byteObj["field"]["name"]
                )
            else:
                print(byteObj["opr"] + "not implemented in" + function)
                return

        case "invoke":
            print("invoke nok implemented")
            print(byteObj)
            print(stack)

            return
        case "load":
            stack.append()
        case "push":
            stack.append(byteObj["value"])
        case "store":
            memory[byteObj["index"]] = {"type": byteObj["type"], "value": stack.pop()}
              """