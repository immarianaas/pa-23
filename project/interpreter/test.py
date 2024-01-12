from Util import Heap, Operand, PrimitiveTypes, StackFrame
from Interpreter import InterpretFunction


dir = "course-02242-examples\decompiled"
file = "dtu\compute\exec\Simple"

assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="noop",
    ).get_value()
    == None
)
assert (
    InterpretFunction(dir=dir, file=file, function="zero", printDebug=True).get_value()
    == 0
)
assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="hundredAndTwo",
    ).get_value()
    == 102
)

stackframe = StackFrame()
stackframe.set(0, operand=Operand(type="int", value=20))

assert (
    InterpretFunction(
        stackFrame=stackframe,
        dir=dir,
        file=file,
        function="identity",
    ).get_value()
    == 20
)


stackframe.set(1, operand=Operand(type="int", value=10))


assert (
    InterpretFunction(
        stackFrame=stackframe,
        dir=dir,
        file=file,
        function="add",
    ).get_value()
    == 30
)


assert (
    InterpretFunction(
        stackFrame=stackframe,
        dir=dir,
        file=file,
        function="min",
    ).get_value()
    == 10
)


assert (
    InterpretFunction(
        stackFrame=stackframe, dir=dir, file=file, function="div"
    ).get_value()
    == 2
)

stackframe2 = StackFrame()
stackframe2.set(0, operand=Operand(type="integer", value=4))


assert (
    InterpretFunction(
        stackFrame=stackframe2,
        dir=dir,
        file=file,
        function="factorial",
        printDebug=True,
    ).get_value()
    == 24
)


file = "dtu\compute\exec\Calls"

stackframe_fib = StackFrame()
stackframe_fib.set(0, operand=Operand(type="int", value=5))
assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="fib",
        stackFrame=stackframe_fib,
    ).get_value()
    == 8
)


"""assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="helloWorld",
    ).get_value()
    == None
)"""


file = "dtu\compute\exec\Array"

assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="newArray",
    ).get_value()
    == 1
)

assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="aWierdOneWithinBounds",
    ).get_value()
    == 1
)
