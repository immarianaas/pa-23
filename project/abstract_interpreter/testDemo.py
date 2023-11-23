from Util import Heap
from abstract_Interpreter import InterpretFunction
from abstraction import abstract_int
import os


this_path = os.path.dirname(os.path.abspath(__file__))
dir = os.path.join(this_path, "..", "..", "demo", "decompiled", "classes")
file = os.path.join("com", "example", "Test")

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


dir = os.path.join(this_path, "..", "pa-app", "decompiled", "classes")
file = os.path.join("dk", "dtu", "pa", "App")

print(os.path.join(dir, file))

main_set = set()
InterpretFunction(
    dir=dir,
    file=file,
    edges=main_set,
    function="appMain",
    printDebug=True,
)

# print(main_set)

main_list = list(main_set)
main_list.sort()


def print_set(sett):
    for tup in main_list:
        print(f"({tup[0].replace('/','.')} , {tup[1].replace('/','.')})")


f = open("project\evaluation\sem.txt", "w")
for tup in main_list:
    f.write(f"({tup[0].replace('/','.')} , {tup[1].replace('/','.')})\n")
f.close()

print_set(main_set)
