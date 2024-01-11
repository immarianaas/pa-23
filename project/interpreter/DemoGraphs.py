import graphviz
from Util import Heap, Operand, OperandStack, PrimitiveTypes, StackFrame
from Interpreter import InterpretFunction

# For window
dir = "demo\decompiled\classes"
file = "com\example\Test"

# For window
f = open("project\Interpreter\demoEdges.txt", "w")


# For linux
# dir = "demo/decompiled/classes"
# file = "com/example/Test"

# For linux
# f = open("project/Interpreter/demoEdges.txt", "w")

dot = graphviz.Digraph(comment="Tests", engine="fdp")

edges = InterpretFunction(
    dir=dir,
    file=file,
    function="test1",
)[1]


edges.update(
    InterpretFunction(
        dir=dir,
        file=file,
        function="test2",
    )[1]
)

edges.update(
    InterpretFunction(
        dir=dir,
        file=file,
        function="test3",
    )[1]
)

edges.update(
    InterpretFunction(
        dir=dir,
        file=file,
        function="test4",
    )[1]
)

edges.update(
    InterpretFunction(
        dir=dir,
        file=file,
        function="test5",
    )[1]
)

edges.update(
    InterpretFunction(
        dir=dir,
        file=file,
        function="test6",
    )[1]
)

for v1, v2 in edges:
    dot.edge(v1, v2)
dot.render("project/Interpreter/diagram")
