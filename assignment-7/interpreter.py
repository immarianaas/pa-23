from dataclasses import dataclass
import os
import json
import glob
import subprocess
from collections import defaultdict
import z3
from z3 import Solver, ExprRef

###########################################################
#                     INITIAL SETUP                       #
###########################################################

# { class_name1:
#   {
#       method1: json data1,
#       method2 : json_data2
#   },
#   class_name2: {},
#   ...
# }
methods_data = defaultdict(dict)


def saveMethodsData(obj):
    global methods_data

    class_name = obj["name"]
    for m in obj["methods"]:
        methods_data[class_name][m["name"]] = m


def setupProjDir(proj_directory: str):
    print(proj_directory)
    for new_filename in glob.iglob(proj_directory + "/**/*.json", recursive=True):
        f = open(new_filename)
        data: json = json.load(f)
        saveMethodsData(data)
        f.close()


setupProjDir(os.path.join(".", "course-02242-examples"))

###########################################################
#                 INTERPRETER + ANALYSIS                  #
###########################################################


@dataclass
class ConcolicValue:
    concrete: int | bool
    symbolic: z3.ExprRef

    def __repr__(self):
        return f"{self.concrete} {self.symbolic}"

    @classmethod
    def from_const(self, c):
        if isinstance(c, bool):
            return ConcolicValue(c, z3.BoolVal(c))

        if isinstance(c, int):
            return ConcolicValue(c, z3.IntVal(c))

        raise Exception(f"Unknown const {c}")

    def binary(self, copr, other):
        DICT = {
            "sub": "__sub__",
            "add": "__add__"
        }

        if copr == "div":
            return ConcolicValue(
                self.concrete // other.concrete,
                z3.simplify(self.symbolic / other.symbolic)
            )

        if copr not in DICT:
            raise Exception(f"Unknown binary operation: {copr}")

        opr = DICT[copr]
        # explanation below!
        return ConcolicValue(
            getattr(self.concrete, opr)(other.concrete),
            z3.simplify(getattr(self.symbolic, opr)(other.symbolic))
        )

    def compare(self, copr, other):
        DICT = {
            "ne": "__ne__",
            "gt": "__gt__",
            "ge": "__ge__"
        }
        if copr not in DICT:
            raise Exception(f"Unknown comparison: {copr}")

        opr = DICT[copr]
        # for the "ne" case:
        # getattr(self.concrete, opr) -- will bascially be transformed into:
        #   `self.concrete.__ne__`
        # and then we are passing an argument: other.concrete

        # basically we are doing:
        # ConcolicValue( self.concrete.__ne__(other.concrete ) )
        return ConcolicValue(
            getattr(self.concrete, opr)(other.concrete),
            z3.simplify(getattr(self.symbolic, opr)(other.symbolic))
        )


@dataclass
class State:
    locals: dict[int, ConcolicValue]
    stack: list[ConcolicValue]

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        return self.stack.pop()

    def load(self, index):
        return self.push(self.locals[index])

    def store(self, index):
        self.locals[index] = self.pop()


@dataclass
class Bytecode:
    dictionary: dict

    def __getattr__(self, name):
        return self.dictionary[name]

    def __repr__(self) -> str:
        return f"{self.opr} " + " | ".join(
            f"{k}: {v}" for k, v in self.dictionary.items() if k != "opr" and k != "value"
        )


def concolic(target, k=1000):
    solver = z3.Solver()

    params = [z3.Int(f"p{i}") for i, p in enumerate(target["params"])]

    while solver.check() == z3.sat:
        model = solver.model()
        input = [model.eval(p, model_completion=True).as_long()
                 for p in params]

        state = State({k: ConcolicValue(i, p) for k, (i, p) in enumerate(zip(input, params))},
                      []
                      )

        bytecode = [Bytecode(b) for b in target["code"]["bytecode"]]
        pc = 0
        path = []

        for _ in range(k):
            bc = bytecode[pc]
            pc += 1
            # print(state)
            # print(bc)
            # print(path)
            # print("-----")

            if bc.opr == "get" and bc.field["name"] == "$assertionsDisabled":
                state.push(ConcolicValue.from_const(False))

            elif bc.opr == "ifz":
                v = state.pop()
                z = ConcolicValue.from_const(0)
                r = ConcolicValue.compare(z, bc.condition, v)

                if r.concrete:
                    pc = bc.target
                    path += [r.symbolic]
                else:
                    path += [z3.simplify(z3.Not(r.symbolic))]

            elif bc.opr == "if":
                v2 = state.pop()
                v1 = state.pop()
                r = ConcolicValue.compare(v1, bc.condition, v2)
                state.push(r)
                if r.concrete:
                    pc = bc.target
                    path += [r.symbolic]
                else:
                    path += [z3.simplify(z3.Not(r.symbolic))]

            elif bc.opr == "new" and bc.dictionary["class"] == "java/lang/AssertionError":
                result = "AssertionError"
                break

            elif bc.opr == "load":
                state.load(bc.index)

            elif bc.opr == "store":
                state.store(bc.index)

            elif bc.opr == "push":
                state.push(ConcolicValue.from_const(bc.value["value"]))

            elif bc.opr == "binary":
                v2 = state.pop()
                v1 = state.pop()

                if bc.operant == "div":
                    if v2.concrete == 0:
                        result = "Divide by 0"
                        path += [v2.symbolic == 0]
                        break
                    else:
                        path += [z3.simplify(z3.Not(v2.symbolic == 0))]

                r = v1.binary(bc.operant, v2)
                state.push(r)

            elif bc.opr == "incr":
                state.load(bc.index)
                v = state.pop()
                state.push(
                    v.binary("add", ConcolicValue.from_const(bc.amount)))
                state.store(bc.index)

            elif bc.opr == "goto":
                pc = bc.target

            elif bc.opr == "return":
                if bc.type is None:
                    result = "return"
                else:
                    result = f"returned {state.pop()}"
                break
            else:
                raise Exception(f"Unsupported bytecode: {bc}")
        else:
            result = "out of iterations"

        path_constraint = z3.simplify(z3.And(*path))
        print(input, "-->", result, "|", path_constraint)
        solver.add(z3.Not(path_constraint))


###########################################################
#                    RUN THE ANALYSIS                     #
###########################################################

def analyseMethod(class_name, method_name):
    if class_name not in methods_data:
        print(f"CLASS NAME {class_name} not found.")
        return

    if method_name not in saveMethodsData[class_name]:
        print(f"METHOD NAME {method_name} not found.")
        return

    return concolic(methods_data[method_name])


analyseMethod("eu/bogoe/dtu/exceptional/Arithmetics",
              "itDependsOnLattice3", None)
