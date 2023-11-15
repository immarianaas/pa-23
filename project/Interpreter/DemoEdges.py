from Util import Heap, Operand, OperandStack, PrimitiveTypes, StackFrame
from Interpreter import InterpretFunction


dir = "demo\decompiled\classes"
file = "com\example\Test"

f = open("project\Interpreter\demoEdges.txt", "w")


f.write(
    str(
        InterpretFunction(
            dir=dir,
            file=file,
            function="test1",
        )[1]
    )
    + "\n"
)


f.write(
    str(
        InterpretFunction(
            dir=dir,
            file=file,
            heap=Heap(),
            function="test2",
        )[1]
    )
    + "\n"
)

f.write(
    str(
        InterpretFunction(
            dir=dir,
            file=file,
            function="test3",
        )[1]
    )
    + "\n"
)

f.write(
    str(
        InterpretFunction(
            dir=dir,
            file=file,
            function="test4",
        )[1]
    )
    + "\n"
)

f.write(
    str(
        InterpretFunction(
            dir=dir,
            file=file,
            function="test5",
        )[1]
    )
    + "\n"
)

f.write(
    str(
        InterpretFunction(
            dir=dir,
            file=file,
            function="test6",
        )[1]
    )
    + "\n"
)
f.close()
