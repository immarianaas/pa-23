import copy
from enum import Enum
import json
import math
import os
from pathlib import Path
import random
import numpy


class PrimitiveTypes(Enum):
    byte = "byte"
    short = "short"
    int = "int"
    integer = "int"
    long = "long"
    float = "float"
    double = "double"
    boolean = "boolean"
    char = "char"
    ref = "ref"


intTypes = [PrimitiveTypes.int, "integer"]


def InterpretFunction(
    dir: str,
    file: str,
    function: str = "main",
    operandStack=[],
    stackFrame={},
    printDebug=False,
):
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
    if printDebug:
        print("\n------------ Interpreting ", fun["name"], " -----------------")
    return interpretBytecode(
        byteArray=byteArray,
        function=obj["name"] + "/" + fun["name"],
        dir=dir,
        stackFrame=stackFrame,
        operandStack=operandStack,
        printDebug=printDebug,
    )


def error():
    print("There was an Error")
    return


def newIndexRef(memory):
    keys = list(memory.keys())
    keys.sort()
    if len(keys) > 0:
        return keys[0] - 1
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
        return  # {"value": random.randrange(9999), "type": "ref"}

    obj = json.load(f)
    fields = obj["fields"]
    field = [f for f in fields if f["name"] == field["name"]][0]
    return field


def interpretBytecode(
    byteArray: [],
    function: str,
    dir,
    operandStack: [],
    stackFrame: dict,
    index: int = 0,
    printDebug=False,
):
    byteObj = byteArray[index]
    if printDebug:
        print(
            "\n    -- ",
            operandStack,
            "\n    -- ",
            stackFrame,
            "\n\n",
            index,
            ":",
            byteObj,
        )
    index = index + 1
    match byteObj["opr"]:
        case "arraylength":
            ref = operandStack.pop()
            operandStack.append(stackFrame[ref["value"]]["value"]["len"])
        case "array_load":
            i = operandStack.pop()["value"]
            ref = operandStack.pop()
            a = stackFrame[ref["value"]]["value"]["content"]
            operandStack.append(a[i])
        case "array_store":
            v = operandStack.pop()
            i = operandStack.pop()
            ref = operandStack.pop()
            stackFrame[ref["value"]]["value"]["content"][i["value"]] = v
        case "binary":
            v2 = operandStack.pop()
            v1 = operandStack.pop()
            assert v1["type"] == v2["type"]
            match byteObj["operant"]:
                case "add":
                    operandStack.append(
                        {"value": v1["value"] + v2["value"], "type": v1["type"]}
                    )
                case "sub":
                    operandStack.append(
                        {"value": v1["value"] - v2["value"], "type": v1["type"]}
                    )
                case "div":
                    operandStack.append(
                        {"value": v1["value"] / v2["value"], "type": v1["type"]}
                    )
                case "mul":
                    operandStack.append(
                        {"value": v1["value"] * v2["value"], "type": v1["type"]}
                    )
                case "rem":
                    operandStack.append(
                        {
                            "value": math.remainder(v1["value"], v2["value"]),
                            "type": v1["type"],
                        }
                    )
                case _:
                    error()
        case "dup":
            vals = operandStack[-byteObj["words"] :]
            operandStack = operandStack[: len(operandStack) - byteObj["words"]]
            for v in vals:
                operandStack.append(v)
                operandStack.append(v)
        case "get":
            if byteObj["static"] == True:
                value = getStaticField(dir=dir, field=byteObj["field"])
                operandStack.append(value)
            else:
                print("get not implemented")
        case "goto":
            index = byteObj["target"]
        case "if":
            v2 = operandStack.pop()
            v1 = operandStack.pop()
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
            v = operandStack.pop()
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
            v = stackFrame[byteObj["index"]]["value"]
            stackFrame[byteObj["index"]]["value"] = v + byteObj["amount"]
        case "invoke":
            method = byteObj["method"]
            num_args = len(method["args"])
            mem = {i: v for i, v in enumerate(operandStack[-num_args:])}
            operandStack = operandStack[: (len(operandStack) - num_args)]
            if byteObj["access"] == "static" and not method["is_interface"]:
                res = InterpretFunction(
                    dir=dir,
                    file=method["ref"]["name"],
                    function=method["name"],
                    operandStack=[],
                    stackFrame=mem,
                    printDebug=printDebug,
                )
                operandStack.append(res)
            else:
                print("Invoke not implementet for case", byteObj)

        case "load":
            operandStack.append(copy.deepcopy(stackFrame[byteObj["index"]]))

        case "newarray":
            ref = malloc()
            i = operandStack.pop()["value"]
            array = {index: {"type": None, "value": None} for index in range(i)}
            stackFrame[ref] = {
                "value": {"content": array, "len": {"type": "integer", "value": i}},
                "type": "integer array",
            }
            operandStack.append({"value": ref, "type": "ref"})
        case "push":
            operandStack.append(byteObj["value"])
        case "return":
            if byteObj["type"] == None:
                return {"type": None, "value": None}
            else:
                res = operandStack.pop()
                # assert res["type"] == byteObj["type"]
                return res
        case "store":
            stackFrame[byteObj["index"]] = operandStack.pop()

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
            operandStack=operandStack,
            stackFrame=stackFrame,
            printDebug=printDebug,
        )
    else:
        return "Error - index out of range"


def malloc():
    return random.randrange(1000, 9999)


class Object:
    def __init__(self):
        self.members = {}
        self.ref_count = 1


class Heap:
    def __init__(self) -> None:
        self.map = {}
        self.next = 0

    def malloc(self, size: int) -> int:
        ptr = self.next
        self.map[ptr] = Object()
        self.next += 1
        return ptr

    def get(self, ptr: int) -> Object:
        return self.map[ptr]

    def inc_count(self, ptr: int) -> None:
        self.map[ptr].ref_count += 1

    def dec_count(self, ptr: int) -> None:
        self.map[ptr].ref_count -= 1
        #  check count and release memory


heap = Heap()


class Operand:
    def __init__(self, value: str | int = None, type: PrimitiveTypes = None) -> None:
        self.map = {"value": value, "type": type}

    def setValue(self, value: str | int) -> None:
        self.map["value"] = value

    def getValue(self) -> str | int:
        return self.map["value"]

    def getType(self) -> PrimitiveTypes:
        return self.map["type"]


class OperandStack:
    def __init__(self) -> None:
        self.stack = []

    def pop(self) -> Operand:
        return self.pop()

    def push(self, val):
        self.append(val)


class StackFrame:
    def __init__(self) -> None:
        self.map = {}

    def get(self, ptr: int) -> Operand:
        return self.map[ptr]

    def set(self, ptr: int, operand: Operand) -> None:
        self.map[ptr] = operand


def min_kode():
    global heap
    ref = heap.malloc(10)
