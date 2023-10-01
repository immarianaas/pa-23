'''
The analysis checks if the abstract state remains zero after k executions, 
which is expected because it is a simple program.

- abtract domain: integer range domain.
- compute fix point that represents abstract state after k executions.
- check if abstract state after k executions is still zero. 
'''

# def abstract_args(m):
#     match m:
#         case "zero":
#             print("zero case")
#             return [0]


def is_error(s):
    return False
# the states are the elements of the set
bc_identity = [
          { "offset": 0, "opr": "load", "type": "int", "index": 0 },
          { "offset": 1, "opr": "return", "type": "int" }
        ]

def abstract_step(bc, state, pc):
    # print(pc, state)
    match state["opr"]:
        case "load":
            return (state["type"], pc+1)
        case "return":
            return (state["type"], pc+1)
   

def bounded_abstract_interpretation(bc, m, k):
    # bc is the bytecode, m is the method, k is the number of iterations
    # s is the state, pc is the program counter, npc is the next program counter
    # ns is the next state, Pc is the program counter class
    s = bc
    # s = { Pc(m, 0) : (abstract_args(m), []) }
    for i in range(0, k):
        list_abstract_join = []
        for pc, state in enumerate(s):
            # next state is the abstract state of the next state
            (ns, npc) = abstract_step(bc, state, pc)
            if is_error(ns):
                return "Has error: " + ns
            list_abstract_join.append(ns)
            print(list_abstract_join)
    # print(s)


    # Add new elements to the set
    # new_m_value = 10
    # s[Pc(new_m_value, 0)] = (abstract_args(new_m_value), [])

bounded_abstract_interpretation(bc_identity, "identity", 1)
bounded_abstract_interpretation(bc_identity, "zero", 1)
