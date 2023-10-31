import json

from Interpreter import InterpretFunction


dir = "course-02242-examples\decompiled"
file = "dtu\compute\exec\Simple"
assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="noop",
        stack=[],
        memory={},
    )
    == None
)
assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="zero",
        stack=[],
        memory={},
    )
    == 0
)
assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="hundredAndTwo",
        stack=[],
        memory={},
    )
    == 102
)
assert (
    InterpretFunction(
        memory={0: {"type": "integer", "value": 20}},
        dir=dir,
        file=file,
        function="identity",
        stack=[],
    )
    == 20
)
assert (
    InterpretFunction(
        memory={
            0: {"type": "integer", "value": 10},
            1: {"type": "integer", "value": 5},
        },
        dir=dir,
        file=file,
        function="add",
        stack=[],
    )
    == 15
)

assert (
    InterpretFunction(
        memory={
            0: {"type": "integer", "value": 10},
            1: {"type": "integer", "value": 5},
        },
        dir=dir,
        file=file,
        function="min",
        stack=[],
    )
    == 5
)

assert (
    InterpretFunction(
        memory={
            0: {"type": "integer", "value": 10},
            1: {"type": "integer", "value": 5},
        },
        dir=dir,
        file=file,
        function="div",
        stack=[],
    )
    == 2
)
