from Util import Heap
from abstract_Interpreter import InterpretFunction
from abstraction import abstract_int
import os 

"""
dir = "demo/decompiled/classes"
file = "com/example/Test"

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

assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="test8",
        # printDebug=True,
    )[0]
    .get_value()
    .size()
    == 0
)


assert InterpretFunction(
    dir=dir,
    file="com/example/Main",
)[0]


"""

this_path = os.path.dirname(os.path.abspath(__file__))

dir = os.path.join(this_path, "..", "pa-app", "decompiled", "classes")
file = os.path.join("dk", "dtu", "pa", "App")

new_set = set()
InterpretFunction(
    dir=dir,
    edges = new_set,
    file=file,
    function="appMain"
)