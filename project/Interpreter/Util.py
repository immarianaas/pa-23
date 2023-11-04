from enum import Enum


def PrimitiveTypes(str: str) -> str:
    match str:
        case "int" | "integer":
            return "int"
        case _:
            if isPrimitiveType(str):
                return str
            RuntimeError("Type not Supported")


def isPrimitiveType(str) -> bool:
    return str in [
        "ref",
        "byte",
        "short",
        "int",
        "integer",
        "long",
        "float",
        "double",
        "boolean",
        "char",
        "string",
    ]


class Object:
    def __init__(self):
        self.content = None
        self.ref_count = 1


class Heap:
    def __init__(self) -> None:
        self.map = {}
        self.counter_map = {}
        self.next = 0

    def malloc(self, object=None) -> int:
        ptr = self.next
        self.map[ptr] = object
        self.counter_map[ptr] = 1
        self.next += 1
        return ptr

    def get(self, ptr: int) -> Object:
        return self.map[ptr]

    def inc_count(self, ptr: int) -> None:
        self.counter_map[ptr] += 1

    def dec_count(self, ptr: int) -> None:
        self.counter_map[ptr] -= 1
        #  check count and release memory


heap = Heap()


class Operand:
    def __init__(self, object={}):
        if "value" in object:
            self.value = object["value"]
        else:
            self.value = None
        if "value" in object:
            self.type = PrimitiveTypes(object["type"])
        else:
            self.type = None

    def set_value(self, value: str | int) -> None:
        self.value = value

    def get_value(self) -> str | int:
        return self.value

    def set_type(self, type) -> PrimitiveTypes:
        self.type = type

    def get_type(self) -> PrimitiveTypes:
        return self.type

    def __str__(self):
        val = str(self.value) if self.value is not None else "None"
        typ = str(self.type) if self.type is not None else "None"
        return "(" + val + ", " + typ + ")"


class OperandStack:
    def __init__(self) -> None:
        self.stack = []

    def pop(self) -> Operand:
        return self.stack.pop()

    def push(self, val: Operand):
        self.stack.append(val)

    def is_empty(self) -> bool:
        return len(self.stack) <= 0

    def __str__(self) -> str:
        return (", ").join([str(o) for o in self.stack])


class StackFrame:
    def __init__(self) -> None:
        self.map = {}

    def get(self, ptr: int) -> Operand:
        return self.map[ptr]

    def set(self, ptr: int, operand: Operand) -> None:
        self.map[ptr] = operand

    def __str__(self) -> str:
        return (", ").join([str(ptr) + ": " + str(self.map[ptr]) for ptr in self.map])


def min_kode():
    global heap
    ref = heap.malloc(10)


def PrintError(byteObj):
    print("##################################################################")
    print(byteObj["opr"] + " not implemented")
    print(byteObj)
    print("##################################################################")


def printStackTrace(operandStack, stackFrame, index, byte_object):
    print(
        "#\n#    -- ",
        operandStack,
        "\n#    -- ",
        stackFrame,
        "\n#\n#",
        index,
        ":",
        byte_object,
    )


class Array:
    def __init__(self, len, dim, type):
        self.len = len
        self.dim = dim
        self.type = type
        self.content = {index: {"type": None, "value": None} for index in range(len)}
