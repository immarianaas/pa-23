from Util import Heap, Operand, OperandStack, PrimitiveTypes, StackFrame
from abstract_Interpreter import InterpretFunction
from abstraction import abstract_int

# For window
dir = "demo\decompiled\classes"
file = "com\example\Test"

# For linux
# dir = "demo/decompiled/classes"
# file = "com/example/Test"


InterpretFunction(
    dir=dir,
    file=file,
    function="test1",
    printDebug=True,
)

assert InterpretFunction(
    dir=dir,
    file=file,
    function="test1",
    printDebug=True,
)[
    0
].get_value() == abstract_int(1)


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

assert InterpretFunction(
    dir=dir,
    file=file,
    function="test3",
    # printDebug=True,
)[0].get_value() == abstract_int(5)

assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="test4",
        # printDebug=True,
    )[0].get_value()
    == None
)

assert InterpretFunction(
    dir=dir,
    file=file,
    function="test5",
    # printDebug=True,
)[0].get_value() == abstract_int(45)

assert InterpretFunction(
    dir=dir,
    file=file,
    function="test6",
    # printDebug=True,
)[0].get_value() == abstract_int(5)
