import json
import os
from pathlib import Path

from createGraph import createGraph


edges = set()


def getAllNodes(dir):
    dir = Path(dir)
    for file in (dir).glob("**/*.json"):
        f = open(file, "r")
        obj = json.load(f)
        methods = obj["methods"]
        for m in methods:
            nodes.add(obj["name"] + "/" + m["name"])


nodes = set()


def InterpretFunction(
    dir: str, file: str, function: str = "main", clas: str = None, stack=[], memory={}
) -> (any, set):
    try:
        f = open(dir + "/" + file + ".json", "r")
        f.close
    except:
        print(file + " not found")
        return None
    obj = json.load(f)
    methods = obj["methods"]
    fun = [f for f in methods if f["name"] == function][0]
    byteArray = fun["code"]["bytecode"]
    return interpretBytecode(
        byteArray=byteArray, function=obj["name"] + "/" + fun["name"], dir=dir
    )


def interpretBytecode(
    byteArray: [], function: str, dir, index: int = 0, stack: [] = [], memory: dict = {}
):
    print(function)
    byteObj = byteArray[index]
    index = index + 1
    match byteObj["opr"]:
        case "return":
            if byteObj["type"] is None:
                return None
            assert len(stack) > 0
            return stack.pop()

        case "push":
            stack.append(byteObj["value"]["value"])

        case "load":
            match byteObj["type"]:
                case "ref" | "int":
                    stack.append(memory[byteObj["index"]])

        case "binary":
            a = stack.pop()
            b = stack.pop()
            match byteObj["operant"]:
                case "add":
                    stack.append(a + b)
                case "mul":
                    stack.append(a * b)
                case "sub":
                    stack.append(a - b)
                case _:
                    print("binary operant", byteObj["condition"], "not implemented")
                    return

        case "if":
            assert len(stack) >= 2
            a = stack.pop()
            b = stack.pop()
            jump = False

            match byteObj["condition"]:
                case "gt":
                    jump = b > a
                case "ge":
                    jump = b >= a
                case "le":
                    jump = b <= a
                case "lt":
                    jump = b < a
                case _:
                    print("if condition", byteObj["condition"], "not implemented")
                    return

            if jump:
                index = byteObj["target"]

        case "ifz":
            assert len(stack) >= 1
            elem = stack.pop()
            jump = False

            match byteObj["condition"]:
                case "le":
                    jump = elem is None or elem <= 0
                case "ne":
                    jump = elem is not None and elem != 0
                case "eq":
                    jump = elem is None or elem == 0
                case _:
                    print("ifz condition", byteObj["condition"], "not implemented")
                    return
            if jump:
                index = byteObj["target"]

        case "store":
            memory[byteObj["index"]] = stack.pop()

        case "incr":
            memory[byteObj["index"]] += byteObj["amount"]
            stack.append(memory[byteObj["index"]])
        case "goto":
            index = byteObj["target"]
        case "array_load":
            index_array = stack.pop()
            array = stack.pop()

            if index_array > len(array):
                raise RuntimeError("Out of bounds.")

            stack.append(array[index_array])

        case "array_store":
            elem = stack.pop()
            index_array = stack.pop()
            array = stack.pop()
            array.append(elem)
            stack.append(array)

        case "newarray":
            stack.append([])

        case "arraylength":
            stack.append(len(stack[-1]))

        case "throw":
            raise RuntimeError("Throwing an exception (incomplete)")

        case "invoke":
            # print(byteObj["access"])
            # print(byteObj)
            # print(stack)
            byteObj["method"]["name"]
            edges.add(
                (
                    function,
                    (
                        byteObj["method"]["ref"]["name"]
                        + "/"
                        + byteObj["method"]["name"]
                    ),
                )
            )
            stack.append(
                InterpretFunction(
                    dir=dir,
                    file=byteObj["method"]["ref"]["name"],
                    function=byteObj["method"]["name"],
                    stack=stack,
                    memory=memory,
                )
            )

        case "get":
            print("TODO - implement get - now from: " + byteObj["field"]["class"])

        case "new":
            stack.append(byteObj["class"])

        case "pop":
            stack = stack[: len(stack) - byteObj["words"]]
        case "dup":
            vals = stack[-byteObj["words"] :]
            stack = stack[: len(stack) - byteObj["words"]]
            for v in vals:
                stack.append(v)
                stack.append(v)

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
        )
    else:
        return "Error - index out of range"


dir = "project/pa-app/decompiled"
getAllNodes(dir)
res = InterpretFunction(dir=dir, file="classes/dk/dtu/pa/App")
print(edges)

# createGraph(nodes=nodes, edges=edges, dir="project/")
