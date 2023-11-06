from Util import Heap, Operand, PrimitiveTypes, StackFrame
from Interpreter import InterpretFunction


dir = "demo\decompiled\classes"
file = "com\example\Test"


assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="test1",
    ).get_value()
    == 1
)


assert (
    InterpretFunction(dir=dir, file=file, function="test2", printDebug=True).get_value()
    == None
)

assert (
    InterpretFunction(dir=dir, file=file, function="test3", printDebug=True).get_value()
    == 43
)
