import copy
from enum import Enum
import json
import math
import os
from pathlib import Path
import random
import numpy
import sys

this_path = os.path.dirname(os.path.abspath(__file__))

sys.path.append(this_path)
from Util import (
    Array,
    Heap,
    Operand,
    OperandStack,
    PrimitiveTypes,
    PrintError,
    StackFrame,
    isPrimitiveType,
    printStackTrace,
)
from abstraction import abstract_int


def InterpretFunction(
    dir: str,
    file: str,
    edges=set(),
    heap: Heap = Heap(),
    function: str = "main",
    stackFrame=StackFrame(),
    printDebug=False,
) -> (Operand, []):
    if printDebug:
        print(
            "---------------- function: ",
            file + "/" + function + " ---------------------------",
        )
    if file == "java/lang/Object" or file == "java/io/PrintStream":
        if printDebug:
            print("----------------------- return ----------------------------------")

        return (Operand(), edges)
    f = open(dir + "/" + file + ".json", "r")
    f.close

    json_object = json.load(f)
    method_list = json_object["methods"]
    method = [f for f in method_list if f["name"] == function][0]

    byte_array = method["code"]["bytecode"]

    return interpretBytecode(
        byte_array=byte_array,
        dir=dir,
        edges=edges,
        operandStack=OperandStack(),
        stackFrame=stackFrame,
        printDebug=printDebug,
        heap=heap,
        function_name=getFunctionAnnotation(file, function, method),
    )


def getFunctionAnnotation(file, function, method):
    args = []
    for p in method["params"]:
        if p["type"].get("base"):
            args.append(p["type"]["base"])
        elif p["type"].get("kind") == "class":
            args.append(p["type"]["name"])
    return file + "/" + function + "(" + ",".join(args) + ")"


def get_static(dir: str, field: {}, heap: Heap):
    t = field.get("type")
    try:
        f = open(dir + "/" + field["class"] + ".json", "r")
        f.close
        json_object = json.load(f)
        field_list = json_object["fields"]
        v = [f for f in field_list if f["name"] == field["name"]][0]["value"]
        if isPrimitiveType(t):
            return Operand(type=t, value=v)
        ptr = heap.malloc({**t, "value": v})
        return Operand(value=ptr, type="ref")
    except:
        if field["class"] == "java/lang/System":
            print("############### JAVA MISSING VALUE ###################")
            if isPrimitiveType(t):
                print("########## Get Not implemented for java system ##############")
            elif t.get("kind") == "class":
                v = heap.malloc()
                return Operand(type="ref", value=v)

        print("########## Get Not implemented ##############")


def interpretBytecode(
    byte_array,
    dir,
    function_name,
    edges,
    operandStack: OperandStack,
    stackFrame: StackFrame,
    printDebug: bool,
    heap: Heap,
    index: int = 0,
    skipGoto: bool = False,
) -> (Operand, []):
    byte_object = byte_array[index]

    if printDebug:
        print("skipgoto:", skipGoto)
        printStackTrace(heap, operandStack, stackFrame, index, byte_object)

    index = index + 1
    match byte_object["opr"]:
        case "array_load":
            i = operandStack.pop().get_value()
            ref = operandStack.pop().get_value()
            a = heap.get(ref)
            operandStack.push(a.content[i])
        case "array_store":
            v = operandStack.pop()
            i = operandStack.pop().get_value()
            ref = operandStack.pop().get_value()
            a = heap.get(ref)
            a.content[i] = v
        case "binary":
            v2 = operandStack.pop()
            v1 = operandStack.pop()
            if not (v1.get_type() == v2.get_type()) or not (
                (v1.get_type() == "integer") or (v1.get_type() == "int")
            ):
                if printDebug:
                    print("Binary type error")
            operand = Operand()
            operand.set_type(PrimitiveTypes("int"))
            match byte_object["operant"]:
                case "add":
                    operand.set_value(v1.get_value().add(v2.get_value()))
                case "sub":
                    operand.set_value(v1.get_value().sub(v2.get_value()))
                case "div":
                    operand.set_value(v1.get_value().div(v2.get_value()))
                case "mul":
                    operand.set_value(v1.get_value().mul(v2.get_value()))
                case "rem":
                    operand.set_value()
                case _:
                    RuntimeError("Binary operation not implemented")
            operandStack.push(operand)
        case "dup":
            w = byte_object["words"]
            operands = [operandStack.pop() for i in range(w)]
            for i in range(w * 2):
                for o in operands:
                    operandStack.push(o)
        case "get":
            if byte_object["static"]:
                operandStack.push(
                    get_static(dir=dir, field=byte_object["field"], heap=heap)
                )
            else:
                ref = operandStack.pop()
                name = byte_object["field"]["name"]
                operandStack.push(heap.get(ref.get_value())["fields"][name])
        case "goto":
            if skipGoto:
                skipGoto = False
            else:
                index = byte_object["target"]
        case "if":
            v2 = operandStack.pop()
            v1 = operandStack.pop()
            print(v1, v2)
            if v1.get_type() == "ref" or v2.get_type() == "ref":
                skipGoto = True
                print("heeeellloooooo")
            elif v1.get_value().size() == None or v2.get_value().size() == None:
                skipGoto = True
            else:
                match byte_object["condition"]:
                    case "eq":
                        if v1.get_value().size() == 0 and v2.get_value().size() == 0:
                            index = byte_object["target"]
                        elif v1.get_value() == v2.get_value():
                            # if they are equal but not 0 then we cannot say whether they are actually equal or not
                            skipGoto = True
                        # if they are not equal then the actual values are not equal
                    case "ne":
                        # if the abstractions are not eqaul, then they are not equal
                        if v1.get_value().size() != v2.get_value().size():
                            index = byte_object["target"]
                        # if the abstractions are eqaul we cannot say whether they are eqaul or not, exept if they are zero
                        elif v1.get_value().size() != 0 and v2.get_value().size() != 0:
                            skipGoto = True
                    case "gt":
                        # if the abstract v1 > abstract v2 then the real v1 > than the real v2
                        if v1.get_value().size() > v2.get_value().size():
                            index = byte_object["target"]
                        #  if they are equal we cannot say anything
                        elif v1.get_value().size() == v2.get_value().size():
                            skipGoto = True
                        # but otherwise we can say that v1 > v2 is false
                    case "ge":
                        # if the abstract v1 > abstract v2 then the real v1 > than the real v2
                        # we can only argue equallity if 0
                        if v1.get_value().size() > v2.get_value().size() or (
                            v1.get_value().size() == 0 and v2.get_value().size() == 0
                        ):
                            index = byte_object["target"]
                        # same as gt
                        elif v1.get_value().size() == v2.get_value().size():
                            skipGoto = True
                    case "lt":
                        if v1.get_value().size() < v2.get_value().size():
                            index = byte_object["target"]
                        elif v1.get_value().size() == v2.get_value().size():
                            skipGoto = True
                    case "le":
                        print("heeeellloooooo2")
                        if v1.get_value().size() < v2.get_value().size() or (
                            v1.get_value().size() == 0 and v2.get_value().size() == 0
                        ):
                            index = byte_object["target"]
                        elif v1.get_value().size() == v2.get_value().size():
                            print("helloo")
                            skipGoto = True
                    case _:
                        RuntimeError("if operation not implemented")
        case "ifz":
            v = operandStack.pop()
            if v.get_type() == "ref":
                skipGoto == True
            elif v.get_value().size() == None:
                skipGoto = True
            else:
                match byte_object["condition"]:
                    case "eq":
                        if v.get_value().size() == 0:
                            index = byte_object["target"]
                    case "ne":
                        if v.get_value().size() != 0:
                            index = byte_object["target"]
                    case "gt":
                        if v.get_value().size() > 0:
                            index = byte_object["target"]
                    case "ge":
                        if v.get_value().size() >= 0:
                            index = byte_object["target"]
                    case "lt":
                        if v.get_value().size() < 0:
                            index = byte_object["target"]
                    case "le":
                        if v.get_value().size() <= 0:
                            index = byte_object["target"]
                    case _:
                        RuntimeError("if operation not implemented")
        case "incr":
            ptr = byte_object["index"]
            o = stackFrame.get(ptr)
            amount = byte_object["amount"]
            v = o.get_value()
            if v.size() == 0:
                o.set_value(abstract_int(amount))
                stackFrame.set(ptr, o)
            elif v.size() == None:
                o.set_value(abstract_int())
            elif (v.size() > 0 and amount < 0) or (v.size() < 0 and amount > 0):
                o.set_value(abstract_int())
        case "invoke":
            access = byte_object["access"]
            method = byte_object["method"]
            arguments = []
            for value in method["args"]:
                if printDebug:
                    print("value: ", value)
                if isinstance(value, dict):
                    arguments.append(value.get("name"))
                elif isinstance(value, str):
                    arguments.append(value)
            function_name2 = (
                method["ref"]["name"]
                + "/"
                + method["name"]
                + "("
                + ",".join(arguments)
                + ")"
            )
            edges.add(
                (
                    str(Path(function_name)).replace("\\", "/"),
                    str(Path(function_name2)).replace("\\", "/"),
                )
            )
            if access == "static":
                sf = StackFrame()
                for i in reversed(range(len(method["args"]))):
                    sf.set(i, operandStack.pop())
                res, e = InterpretFunction(
                    dir=dir,
                    file=method["ref"]["name"],
                    function=method["name"],
                    stackFrame=sf,
                    heap=heap,
                    printDebug=printDebug,
                    edges=edges,
                )
                edges.update(e)
                if res.get_value() is not None:
                    operandStack.push(res)

            elif access == "virtual" or access == "interface":
                args = [operandStack.pop() for _ in method["args"]]
                ref = operandStack.pop()
                object = heap.get(ref.get_value())
                sf = StackFrame()
                sf.add(ref)
                for a in args:
                    sf.add(a)
                res, e = InterpretFunction(
                    dir=dir,
                    file=object["class"],
                    function=method["name"],
                    stackFrame=sf,
                    heap=heap,
                    printDebug=printDebug,
                    edges=edges,
                )
                edges.update(e)
                if res.get_value() is not None:
                    operandStack.push(res)

            elif access == "special":
                args = [operandStack.pop() for _ in method["args"]]
                ref = operandStack.pop()
                sf = StackFrame()
                sf.add(ref)
                for a in args:
                    sf.add(a)
                res, e = InterpretFunction(
                    dir=dir,
                    file=method["ref"]["name"],
                    function=method["name"],
                    stackFrame=sf,
                    heap=heap,
                    printDebug=printDebug,
                    edges=edges,
                )
                edges.update(e)
                if res.get_value() is not None:
                    operandStack.push(res)

            else:
                PrintError(byteObj=byte_object)
                return
        case "load":
            object = stackFrame.get(byte_object["index"])
            # assert object.get_type() == PrimitiveTypes(byte_object["type"])
            operandStack.push(copy.deepcopy(object))
        case "negate":
            o = operandStack.pop()
            v = o.get_value()
            if v.size() == None:
                operandStack.push(Operand(abstract_int(), "int"))
            elif v.size() == 0:
                operandStack.push(Operand(abstract_int(0), "int"))
            elif v.size() > 0:
                operandStack.push(Operand(abstract_int(-1), "int"))
            else:
                operandStack.push(Operand(abstract_int(1), "int"))
        case "new":
            ptr = heap.malloc()
            file = byte_object["class"]
            if file == "java/lang/Object":
                heap.set(ptr, {"class": file, "fields": {}})
            else:
                f = open(dir + "/" + file + ".json", "r")
                f.close
                json_object = json.load(f)
                fields = {}
                for f in json_object["fields"]:
                    fields[f["name"]] = f["value"]
                heap.set(ptr, {"class": file, "fields": fields})
            operandStack.push(Operand(value=ptr, type="ref"))
        case "newarray":
            lenght = operandStack.pop().get_value()
            a = Array(len=lenght, dim=byte_object["dim"], type=byte_object["type"])
            ptr = heap.malloc(object=a)
            o = Operand()
            o.set_type("ref")
            o.set_value(ptr)
            operandStack.push(o)
        case "pop":
            for i in range(byte_object["words"]):
                operandStack.pop()
        case "push":
            value = byte_object["value"]
            operand = Operand(type=value["type"], value=abstract_int(value["value"]))
            operandStack.push(operand)
        case "put":
            if byte_object["static"]:
                PrintError(byte_object)
            else:
                v = operandStack.pop()
                ref = operandStack.pop()
                name = byte_object["field"]["name"]
                heap.get(ref.get_value())["fields"][name] = v
        case "return":
            print(len(byte_array), index, skipGoto)
            if byte_object["type"] == None:
                if not operandStack.is_empty():
                    operandStack.pop()
                if not skipGoto or (index >= len(byte_array) - 1):
                    if printDebug:
                        print(
                            "----------------------- ",
                            function_name,
                            " return ----------------------------------",
                        )
                    return (Operand(), edges)
            else:
                o = operandStack.pop()
                if not skipGoto or (index >= len(byte_array) - 1):
                    if printDebug:
                        print(
                            "----------------------- ",
                            function_name,
                            " return ----------------------------------",
                        )
                    return (o, edges)
        case "store":
            operand = operandStack.pop()
            stackFrame.set(byte_object["index"], operand)
        case _:
            PrintError(byte_object)
            RuntimeError("Case Not implemented")
            return

    if len(byte_array) <= index:
        print("errororororororororororo")
        return "Error - index out of range"
    return interpretBytecode(
        byte_array=byte_array,
        dir=dir,
        function_name=function_name,
        operandStack=operandStack,
        stackFrame=stackFrame,
        index=index,
        printDebug=printDebug,
        heap=heap,
        edges=edges,
        skipGoto=skipGoto,
    )
