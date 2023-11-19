from abstract_interpreter.abstract_Interpreter import (
    InterpretFunction as abstractInterpret,
)
from Interpreter.Interpreter import InterpretFunction

dir = "demo\decompiled\classes"
file = "com\example\Main"

concrete_edges = InterpretFunction(dir=dir, file=file)

abstract_edges = abstractInterpret(
    dir=dir,
    file=file,
)


print(abstract_edges[1] - concrete_edges[1])
