import copy
from enum import Enum
import json
import math
import os
from pathlib import Path
import random
import numpy

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


def InterpretFunction(
    dir: str,
    file: str,
    heap: Heap = Heap(),
    function: str = "main",
    operandStack=OperandStack(),
    stackFrame=StackFrame(),
    printDebug=False,
):
    f = open(dir + "/" + file + ".json", "r")
    f.close
    json_object = json.load(f)
    method_list = json_object["methods"]
    method = [f for f in method_list if f["name"] == function][0]
    byte_array = method["code"]["bytecode"]

    return interpretBytecode(
        byte_array=byte_array,
        dir=dir,
        operandStack=operandStack,
        stackFrame=stackFrame,
        printDebug=printDebug,
        heap=heap,
    )


def get_static(dir: str, field: {}, heap: Heap):
    t = field.get("type")
    o = Operand()
    try:
        f = open(dir + "/" + field["class"] + ".json", "r")
        f.close
        json_object = json.load(f)
        field_list = json_object["fields"]
        v = [f for f in field_list if f["name"] == field["name"]][0]["value"]
        if isPrimitiveType(t):
            o.set_type(t)
            o.set_value(v)
            return o
        RuntimeError("Ref not implemented ")
    except:
        if field["class"] == "java/lang/System":
            if isPrimitiveType(t):
                RuntimeError("Not implemented")
            elif t.get("kind") == "class":
                o.set_type("ref")
                v = heap.malloc()
                o.set_value(v)
                # TODO add value to ref
                return o
            RuntimeError("Not Impelmented")


def interpretBytecode(
    byte_array,
    dir,
    operandStack: OperandStack,
    stackFrame: StackFrame,
    printDebug: bool,
    heap: Heap,
    index: int = 0,
):
    byte_object = byte_array[index]

    if printDebug:
        printStackTrace(operandStack, stackFrame, index, byte_object)

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
            # assert v1.get_type() == v2.get_type()
            # assert v1.get_type() == PrimitiveTypes("int")
            operand = Operand()
            operand.set_type(PrimitiveTypes("int"))
            match byte_object["operant"]:
                case "add":
                    operand.set_value(v1.get_value() + v2.get_value())
                case "sub":
                    operand.set_value(v1.get_value() - v2.get_value())
                case "div":
                    operand.set_value(v1.get_value() / v2.get_value())
                case "mul":
                    operand.set_value(v1.get_value() * v2.get_value())
                case "rem":
                    operand.set_value(math.remainder(v1.get_value() + v2.get_value()))
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
                PrintError(byte_object)
                return
        case "goto":
            index = byte_object["target"]
        case "if":
            v2 = operandStack.pop()
            v1 = operandStack.pop()
            # assert v1.get_type() == v2.get_type()
            # assert v1.get_type() == PrimitiveTypes("int")
            match byte_object["condition"]:
                case "eq":
                    if v1.get_value() == v2.get_value():
                        index = byte_object["target"]
                case "ne":
                    if v1.get_value() != v2.get_value():
                        index = byte_object["target"]
                case "gt":
                    if v1.get_value() > v2.get_value():
                        index = byte_object["target"]
                case "ge":
                    if v1.get_value() >= v2.get_value():
                        index = byte_object["target"]
                case "lt":
                    if v1.get_value() < v2.get_value():
                        index = byte_object["target"]
                case "le":
                    if v1.get_value() <= v2.get_value():
                        index = byte_object["target"]
                case _:
                    RuntimeError("if operation not implemented")
        case "ifz":
            v = operandStack.pop()
            zero = 0 if v.get_type() == PrimitiveTypes("int") else None
            match byte_object["condition"]:
                case "eq":
                    if v.get_value() == zero:
                        index = byte_object["target"]
                case "ne":
                    if v.get_value() != zero:
                        index = byte_object["target"]
                case "gt":
                    if v.get_value() > zero:
                        index = byte_object["target"]
                case "ge":
                    if v.get_value() >= zero:
                        index = byte_object["target"]
                case "lt":
                    if v.get_value() < zero:
                        index = byte_object["target"]
                case "le":
                    if v.get_value() <= zero:
                        index = byte_object["target"]
                case _:
                    RuntimeError("if operation not implemented")
        case "incr":
            amount = byte_object["amount"]
            ptr = byte_object["index"]
            o = stackFrame.get(ptr)
            v = o.get_value()
            o.set_value(v + amount)
            stackFrame.set(ptr, o)
        case "invoke":
            access = byte_object["access"]
            method = byte_object["method"]
            if access == "static":
                sf = StackFrame()
                for i in reversed(range(len(method["args"]))):
                    sf.set(i, operandStack.pop())

                res = InterpretFunction(
                    dir=dir,
                    file=method["ref"]["name"],
                    function=method["name"],
                    stackFrame=sf,
                    heap=heap,
                    printDebug=printDebug,
                )
                operandStack.push(res)
            elif access == "virtual":
                ref = operandStack.pop()
                sf = StackFrame()
                for i in reversed(range(len(method["args"]))):
                    sf.set(i, operandStack.pop())
                if method["ref"]["name"] == "java/io/PrintStream":
                    operandStack.push(Operand())

            else:
                PrintError(byteObj=byte_object)
                return
        case "load":
            object = stackFrame.get(byte_object["index"])
            # assert object.get_type() == PrimitiveTypes(byte_object["type"])
            operandStack.push(copy.deepcopy(object))
        case "newarray":
            lenght = operandStack.pop().get_value()
            a = Array(len=lenght, dim=byte_object["dim"], type=byte_object["type"])
            ptr = heap.malloc(object=a)
            o = Operand()
            o.set_type("ref")
            o.set_value(ptr)
            operandStack.push(o)
        case "push":
            value = byte_object["value"]
            operand = Operand(value)
            operandStack.push(operand)
        case "return":
            if operandStack.is_empty():
                return Operand()
            else:
                return operandStack.pop()
        case "store":
            operand = operandStack.pop()
            stackFrame.set(byte_object["index"], operand)
        case _:
            PrintError(byte_object)
            return

    if len(byte_array) <= index:
        return "Error - index out of range"
    return interpretBytecode(
        byte_array=byte_array,
        dir=dir,
        operandStack=operandStack,
        stackFrame=stackFrame,
        index=index,
        printDebug=printDebug,
        heap=heap,
    )


InterpretFunction(dir="project\pa-app\decompiled\classes", file="dk\dtu\pa\App")
