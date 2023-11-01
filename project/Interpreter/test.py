

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
    )["value"]
    == None
)
assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="zero",
        stack=[],
        memory={},
    )["value"]
    == 0
)
assert (
    InterpretFunction(
        dir=dir,
        file=file,
        function="hundredAndTwo",
        stack=[],
        memory={},
    )["value"]
    == 102
)
assert (
    InterpretFunction(
        memory={0: {"type": "integer", "value": 20}},
        dir=dir,
        file=file,
        function="identity",
        stack=[],
    )["value"]
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
    )["value"]
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
    )["value"]
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
    )["value"]
    == 2
)

assert (
    InterpretFunction(
        memory={
            0: {"type": "integer", "value": 4},
        },
        dir=dir,
        file=file,
        function="factorial",
        stack=[],
    )["value"]
    == 24
)

file = "dtu\compute\exec\Calls"


assert(   InterpretFunction(
        dir=dir,
        file=file,
        function="fib",
        stack=[],
        memory={0: {'type': 'integer', 'value': 5}},
    )["value"] == 8
 ) 

"""
assert(   InterpretFunction(
        dir=dir,
        file=file,
        function="helloWorld",
        stack=[],
        memory={},
        printDebug=True
    )["value"] == None
 ) 
 """


file = "dtu\compute\exec\Array"

assert(   InterpretFunction(
        dir=dir,
        file=file,
        function="newArray",
        stack=[],
        memory={},
           printDebug=True
    )["value"] == 1
 ) 
assert(   InterpretFunction(
        dir=dir,
        file=file,
        function="first",
        stack=[],
        memory={4198: {'value': {'content': {0: {'type': 'integer', 'value': 1}, 1: {'type': 'integer', 'value': 2}, 2: {'type': 'integer', 'value': 3}}, 'len': {'type': 'integer', 'value': 3}}, 'type': 'integer array'}, 0: {'value': 4198, 'type': 'ref'}},
    )["value"] == 1
 ) 
assert(   InterpretFunction(
        dir=dir,
        file=file,
        function="firstSafe",
        stack=[],
        memory={4198: {'value': {'content': {0: {'type': 'integer', 'value': 1}, 1: {'type': 'integer', 'value': 2}, 2: {'type': 'integer', 'value': 3}}, 'len': {'type': 'integer', 'value': 3}}, 'type': 'integer array'}, 0: {'value': 4198, 'type': 'ref'}},
     
    )["value"] == 1
 ) 
assert(   InterpretFunction(
        dir=dir,
        file=file,
        function="bubbleSort",
        stack=[],
        memory={4198: {'value': {'content': {0: {'type': 'integer', 'value': 1}, 1: {'type': 'integer', 'value': 2}, 2: {'type': 'integer', 'value': 3}}, 'len': {'type': 'integer', 'value': 3}}, 'type': 'integer array'}, 0: {'value': 4198, 'type': 'ref'}},
    
        )["value"] == None
 ) 

assert(   InterpretFunction(
        dir=dir,
        file=file,
        function="aWierdOneWithinBounds",
        stack=[],
        memory={},
    )["value"] == 1
 ) 