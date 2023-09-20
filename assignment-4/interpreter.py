import os
import json
import glob
import subprocess


def interpret(obj, function_name, memory):

    method = [m for m in obj["methods"] if m["name"] == function_name]

    assert (len(method) == 1)

    return interpretBytecode(method[0]["code"]["bytecode"], memory=memory, full_data=obj)


def interpretBytecode(byteArray, index=0, stack=[], memory={}, full_data=None):
    byteObj = byteArray[index]
    match byteObj["opr"]:
        case "return":
            if byteObj["type"] is None:
                return None
            assert (len(stack) > 0)
            return stack.pop()

        case "push":
            stack.append(byteObj["value"]["value"])

        case "load":
            stack.append(memory[byteObj["index"]])

        case "binary":
            a = stack.pop()
            b = stack.pop()
            match byteObj["operant"]:
                case "add":
                    stack.append(a+b)
                case "mul":
                    stack.append(a*b)
                case "sub":
                    print("a", a, " b", b)
                    stack.append(a-b)

        case "if":
            assert (len(stack) >= 2)
            a = stack.pop()
            b = stack.pop()
            jump = False

            match byteObj["condition"]:
                case "gt":
                    jump = b > a
                case "ge":
                    jump = b >= a
                case "le":
                    jump = b <= a

            if jump:
                return interpretBytecode(byteArray, byteObj["target"], stack, memory, full_data)

        case "ifz":
            assert (len(stack) >= 1)
            a = stack.pop()
            jump = False

            match byteObj["condition"]:
                case "le":
                    jump = a is None or a <= 0

            if jump:
                return interpretBytecode(byteArray, byteObj["target"], stack, memory, full_data)

        case "store":
            memory[byteObj["index"]] = stack.pop()
        case "new":
            print(byteObj["opr"] + " not implemented")
            return
        case "dup":
            print(byteObj["opr"] + " not implemented")
            return
        case "put":
            print(byteObj["opr"] + " not implemented")
            return
        case "invoke":
            to_invoke = byteObj["method"]

            print(stack)

            num_args = len(to_invoke["args"])
            args = stack[-num_args:]
            stack = stack[:-num_args]

            a = dict(enumerate(args))
            print(a)
            res = interpret(full_data, to_invoke["name"], dict(enumerate(args)))
            stack.append(res)

        case "incr":
            memory[byteObj["index"]] += byteObj["amount"]
            stack.append(memory[byteObj["index"]])
        case "goto":
            return interpretBytecode(byteArray, byteObj["target"], stack, memory, full_data)
        case _:
            print(byteObj["opr"] + " not implemented")
            return

    if (len(byteArray) > index):
        return interpretBytecode(byteArray, index+1, stack, memory, full_data)
    else:
        return "something"


def interpretProjDir(proj_directory: str):
    for file in glob.iglob(proj_directory + "/**/*.class", recursive=True):
        new_filename = "." + file.split('.')[1] + ".json"
        # ret = subprocess.run(["jvm2json", "-s", file, "-t", new_filename ])

        if "Calls.json" not in new_filename:
            continue

        f = open(new_filename)
        data: json = json.load(f)
        f.close()
        return data


