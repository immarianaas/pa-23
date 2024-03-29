from Util import Heap, Operand, OperandStack, PrimitiveTypes, StackFrame
from Interpreter import InterpretFunction
import os

this_path = os.path.dirname(os.path.abspath(__file__))
dir = os.path.join(this_path, "..", "..", "demo", "decompiled", "classes")
file = os.path.join("com", "example", "Test")

# file = os.path.join(dir, "com", "example", "Test")

# For window
# dir = "demo\decompiled\classes"
# file = "com\example\Test"

# For linux
# dir = "demo/decompiled/classes"
# file = "com/example/Test"

"""test1_set = set()
InterpretFunction(
    dir=dir,
    file=file,
    edges = test1_set,
    function="test1",
    #printDebug=True,
)

assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="test1",
        #printDebug=True,
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


test6_set = set()
assert (
    InterpretFunction(
        dir=dir,
        file=file,
        edges= test6_set,
        function="test6",
        # printDebug=True,
    )[0].get_value()
    == 5
)

print("\n\n\n")
print(test1_set)


print("\n\n\n")
print(test6_set)
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
    # printDebug=True,
)

# print(main_set)

main_list = list(main_set)
main_list.sort()


def print_set(sett):
    for tup in main_list:
        print(f"({tup[0].replace('/','.')} , {tup[1].replace('/','.')})")


f = open("project\evaluation\\true.txt", "w")
for tup in main_list:
    f.write(f"({tup[0].replace('/','.')} , {tup[1].replace('/','.')})\n")
f.close()

print_set(main_set)
