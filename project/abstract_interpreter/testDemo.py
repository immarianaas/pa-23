from Util import Heap
from abstract_Interpreter import InterpretFunction
from abstraction import abstract_int

# For window
dir = "demo\decompiled\classes"
file = "com\example\Test"

# For linux
# dir = "demo/decompiled/classes"
# file = "com/example/Test"

assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="test1",
    )[0]
    .get_value()
    .size()
    == abstract_int(1).size()
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
    )[0]
    .get_value()
    .size()
    == abstract_int(5).size()
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
    )[0]
    .get_value()
    .size()
    == abstract_int(45).size()
)

assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="test6",
        # printDebug=True,
    )[0]
    .get_value()
    .size()
    == abstract_int(5).size()
)
