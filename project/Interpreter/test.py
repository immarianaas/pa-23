from Util import Operand, PrimitiveTypes, StackFrame
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
    InterpretFunction(
        dir=dir,
        file=file,
        function="zero",
    ).get_value()
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
stackframe.set(0, operand=Operand({"type": "int", "value": 20}))

assert (
    InterpretFunction(
        stackFrame=stackframe,
        dir=dir,
        file=file,
        function="identity",
    ).get_value()
    == 20
)


stackframe.set(1, operand=Operand({"type": "int", "value": 10}))


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
stackframe2.set(0, operand=Operand({"type": "int", "value": 4}))


assert (
    InterpretFunction(
        stackFrame=stackframe2,
        dir=dir,
        file=file,
        function="factorial",
    ).get_value()
    == 24
)


file = "dtu\compute\exec\Calls"

stackframe_fib = StackFrame()
stackframe_fib.set(0, operand=Operand({"type": "int", "value": 5}))
assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="fib",
        stackFrame=stackframe_fib,
    ).get_value()
    == 8
)


assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="helloWorld",
    ).get_value()
    == None
)


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

"""

assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="first",
        operandStack=[],
        stackFrame={
            4198: {
                "value": {
                    "content": {
                        0: {"type": "integer", "value": 1},
                        1: {"type": "integer", "value": 2},
                        2: {"type": "integer", "value": 3},
                    },
                    "len": {"type": "integer", "value": 3},
                },
                "type": "integer array",
            },
            0: {"value": 4198, "type": "ref"},
        },
    ).get_value()
    == 1
)
assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="firstSafe",
        operandStack=[],
        stackFrame={
            4198: {
                "value": {
                    "content": {
                        0: {"type": "integer", "value": 1},
                        1: {"type": "integer", "value": 2},
                        2: {"type": "integer", "value": 3},
                    },
                    "len": {"type": "integer", "value": 3},
                },
                "type": "integer array",
            },
            0: {"value": 4198, "type": "ref"},
        },
    ).get_value()
    == 1
)
assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="bubbleSort",
        operandStack=[],
        stackFrame={
            4198: {
                "value": {
                    "content": {
                        0: {"type": "integer", "value": 1},
                        1: {"type": "integer", "value": 2},
                        2: {"type": "integer", "value": 3},
                    },
                    "len": {"type": "integer", "value": 3},
                },
                "type": "integer array",
            },
            0: {"value": 4198, "type": "ref"},
        },
    ).get_value()
    == None
)

assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="aWierdOneWithinBounds",
        operandStack=[],
        stackFrame={},
    ).get_value()
    == 1
)
 """

InterpretFunction(
    dir="project\pa-app\decompiled\classes", file="dk\dtu\pa\App", printDebug=True
)
