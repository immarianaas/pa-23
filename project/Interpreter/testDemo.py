from Util import Heap, Operand, OperandStack, PrimitiveTypes, StackFrame
from Interpreter import InterpretFunction


dir = "demo\decompiled\classes"
file = "com\example\Test"


assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="test1",
        printDebug=True,
    )[0].get_value()
    == 1
)


assert (
    InterpretFunction(
        dir=dir,
        file=file,
        heap=Heap(),
        function="test2",
        # printDebug=True,
    )[0].get_value()
    == None
)

assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="test3",
        # printDebug=True,
    )[0].get_value()
    == 5
)

assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="test4",
        # printDebug=True,
    )[0].get_value()
    == None
)

assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="test5",
        # printDebug=True,
    )[0].get_value()
    == 45
)

assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="test6",
        # printDebug=True,
    )[0].get_value()
    == 5
)
