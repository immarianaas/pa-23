import copy
from enum import Enum
import json
import math
import os
from pathlib import Path
import random
import numpy

from Util import (
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
    )


def get_static(dir, field):
    try:
        f = open(dir + "/" + field["class"] + ".json", "r")
        f.close
        json_object = json.load(f)
        field_list = json_object["fields"]
        field2 = [f for f in field_list if f["name"] == field["name"]][0]
        o = Operand()
        if isPrimitiveType(field["type"]):
            o.set_type(field["type"])
            o.set_value(field2["value"])
            return o

    except:
        pass


def interpretBytecode(
    byte_array,
    dir,
    operandStack: OperandStack,
    stackFrame: StackFrame,
    printDebug: bool,
    index: int = 0,
):
    byte_object = byte_array[index]

    if printDebug:
        printStackTrace(operandStack, stackFrame, index, byte_object)

    index = index + 1
    match byte_object["opr"]:
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
        case "get":
            if byte_object["static"]:
                operandStack.push(get_static(dir=dir, field=byte_object["field"]))
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
            print(v.get_value())
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
            if byte_object["access"] == "static":
                method = byte_object["method"]
                sf = StackFrame()
                for i in reversed(range(len(method["args"]))):
                    sf.set(i, operandStack.pop())

                res = InterpretFunction(
                    dir=dir,
                    file=method["ref"]["name"],
                    function=method["name"],
                    stackFrame=sf,
                    printDebug=printDebug,
                )
                operandStack.push(res)
        case "load":
            object = stackFrame.get(byte_object["index"])
            # assert object.get_type() == PrimitiveTypes(byte_object["type"])
            operandStack.push(copy.deepcopy(object))
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
    )
