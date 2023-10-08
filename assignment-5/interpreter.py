from enum import Enum
import os
import json
import glob
import subprocess
from collections import defaultdict
import math

classToMethods = defaultdict(list)

Exception = Enum('Exception',['ArithmeticException'])




def max(range: list):
    max_bounds = [elem[1] for elem in range]
    return max(max_bounds)


def min(range: list):
    min_bounds = [elem[0] for elem in range]
    return max(min_bounds)


def invert(range: list):
    inv = [(-elem[1], -elem[0]) for elem in range]
    return inv


def sum(range_a: list, range_b: list):
    res = [(a[0] + b[0], a[1] + b[1]) for a in range_a for b in range_b]
    return res


def is_incl(value: float, range: list):
    for t in range:
        if min(t) <= 0 <= max(t):
            return True
    return False


def is_exact(value: float, range: list):
    for t in range:
        if min(t) != max(t):
            return False
        if min(t) != value:
            return False
    return True


def saveClassMethods(obj):
    global classToMethods

    classToMethods[obj["name"]] = {}

    for m in obj["methods"]:
        if "code" not in m or m["code"] is None:
            continue

        classToMethods[obj["name"]][m["name"]] = {
            "bytecode": m["code"]["bytecode"],
            "params": [param["type"] for param in m["params"]]
        }

    # class fields
    for field in obj["fields"]:
        classToMethods[obj["name"]][field["name"]] = field["value"]


def getVarValue(class_name, var_name):
    if var_name == "$assertionsDisabled":
        return False

    if class_name not in classToMethods:
        print(f"CLASS NAME {class_name} not found.")
        return

    if var_name not in classToMethods[class_name]:
        print(f"VARIABLE NAME {var_name} not found.")

    value = classToMethods[class_name][var_name]
    return value


def interpretMethod(class_name, method_name, exceptions=[]) -> tuple:
    if class_name not in classToMethods:
        print(f"CLASS NAME {class_name} not found.")
        return

    assert method_name in classToMethods[class_name]

    m = classToMethods[class_name][method_name]

    bytecode = m["bytecode"]
    params = m["params"]

    arguments = []
    for t in params:
        match t["base"]:
            case "int":
                arguments.append([(-math.inf, +math.inf)])
            case "float":
                arguments.append([(-math.inf, +math.inf)])

            case _:
                print("ARGUMENT TYPE NOT SUPPORTED")
                assert False

    # print( list(m.values())[0] )
    ret = interpretBytecode(list(bytecode), memory=dict(
        enumerate(arguments)), exceptions=exceptions)
    return (ret, exceptions)


def interpretBytecode(byteArray, index=0, stack=[], memory={}, exceptions=[], is_assert=False):
    byteObj = byteArray[index]
    match byteObj["opr"]:
        case "return":
            if len(stack) == 0:
                return None
            return stack.pop()

        case "push":
            # stack = [
            #   (type, [ (a1, b1), (a2, b2), ... ])
            # ]
            stack.append([
                         (byteObj["value"]["value"], byteObj["value"]["value"])
                         ])

        case "load":
            stack.append(memory[byteObj["index"]])

        case "binary":
            a_ranges = stack.pop()
            b_ranges = stack.pop()

            match byteObj["operant"]:
                case "add":
                    # stack.append(a+b)
                    print("operant", byteObj["operant"], "not implemented")

                case "mul":
                    # stack.append(a*b)
                    print("operant", byteObj["operant"], "not implemented")

                case "sub":
                    stack.append(sum(a_ranges, invert(b_ranges)))
                    # stack.append(a-b)

                case "div":
                    stack.append([])  # array to store results
                    for i in a_ranges:
                        if (i[0] <= 0 <= i[1]):
                            exceptions.append(
                                (index, Exception.ArithmeticException))

                            if i[0] < 0:
                                stack[-1].append((i[0], -1))
                            if i[1] > 0:
                                stack[-1].append((1, i[1]))

                        else:
                            stack[-1].append(i)
                case _:
                    print("operant", byteObj["operant"], "not implemented")
                    return

        case "if":
            assert (len(stack) >= 2)
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
                return exceptions + interpretBytecode(byteArray, byteObj["target"], stack, memory, exceptions)

        case "ifz":
            assert (len(stack) >= 1)
            value = stack.pop()
            jump = False
            not_jump_too = True

            match byteObj["condition"]:
                case "le":
                    for (a,b) in value:
                        if a<0: 
                            jump = True 
                            
                case "ne":
                    # just for reference, might be useful above
                    # jump = ranges != [] and ranges is not None and not is_incl(0, ranges)
                    # not_jump_too = ranges == [] or ranges is None and is_incl(0, ranges)

                    jump = value is not None and value != bool(0)
                case _:
                    print("ifz condition", byteObj["condition"], "not implemented")
                    return
            # print("jump:", jump)
            # print(byteObj)
            if jump:
                # print(byteObj)
                return interpretBytecode(byteArray, byteObj["target"], stack, memory, exceptions)

                # if not not_jump_too:
                #     return ret1

                # ret2 = interpretBytecode(byteArray, index+1, stack, memory, exceptions)
                # return ( ret1[0]+ret2[0], ret1[1]+ret2[1] )

        case "store":
            memory[byteObj["index"]] = stack.pop()
        case "new":
            pass
            # print(byteObj["opr"] + " not implemented")
            # return
        case "put":
            print(byteObj["opr"] + " not implemented")
            return
        case "invoke":
            to_invoke = byteObj["method"]

            if to_invoke["name"] != "<init>":
                num_args = len(to_invoke["args"])
                args = stack[-num_args:]
                stack = stack[:-num_args]

                res = interpretMethod(
                    to_invoke["ref"]["name"], to_invoke["name"], exceptions=exceptions)
                stack.append(res[0])
            else:
                #print("invoked a <init> ... ignored.")
                pass  # nothing for now..?

        case "incr":
            memory[byteObj["index"]] = sum(memory[byteObj["index"]], [
                                           (byteObj["amount"], byteObj["amount"])])
            # memory[byteObj["index"]] += byteObj["amount"]
            stack.append(memory[byteObj["index"]])
        case "goto":
            # print(byteArray)
            # print( byteObj["target"], '\n')
            return interpretBytecode(byteArray, byteObj["target"], stack, memory, exceptions)
        case "array_load":
            index_array = stack.pop()
            array = stack.pop()

            if index_array > len(array):
                raise RuntimeError("Out of bounds.")

            stack.append(array[index_array])

        case "array_store":
            # print(stack)
            elem = stack.pop()
            index_array = stack.pop()
            array = stack.pop()
            array.append(elem)
            stack.append(array)

        case "get":
            if byteObj["field"]["name"] == "$assertionsDisabled":
                is_assert = True

            value = getVarValue(
                byteObj["field"]["class"], byteObj["field"]["name"])
            stack.append(value)

        case "newarray":
            # stack.append([[], byteObj["dim"]]) # list 2 elements: (array, size)
            stack.append([])  # list 2 elements: (array, size)

        case "dup":
            if byteObj["words"] != 1:
                print(byteObj["opr"] + " not implemented (for words > 1)")
            # stack.append( stack[-1] )

        case "arraylength":
            stack.append(len(stack[-1]))
        
        case "negate":
            value = stack.pop()
            negated = [(-1*b, -1*a) for (a,b) in value]
            stack.append(negated)

        case "throw":
            is_assert = False

            # print(stack)
            # raise RuntimeError("Throwing an exception (incomplete)")

        case _:
            print(byteObj["opr"] + " not implemented")
            return

    # print(byteArray)
    if (len(byteArray) > index):
        return interpretBytecode(byteArray, index+1, stack, memory, exceptions)
    else:
        return "something"


def interpretProjDir(proj_directory: str):
    # print(proj_directory)
    for new_filename in glob.iglob(proj_directory + "/**/*.json", recursive=True):
        f = open(new_filename)
        data: json = json.load(f)
        saveClassMethods(data)
        f.close()



