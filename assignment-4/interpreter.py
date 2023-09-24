import os
import json
import glob
import subprocess
from collections import defaultdict

classToMethods = defaultdict(list)


def saveClassMethods(obj):
    global classToMethods

    for m in obj["methods"]:
        if "code" not in m or m["code"] is None:
            continue
        classToMethods[obj["name"]].append({m["name"]: m["code"]["bytecode"]})

    for field in obj["fields"]:
        classToMethods[obj["name"]].append({field["name"]: field["value"]})

def getVarValue( class_name, var_name ):
    if class_name not in classToMethods:
        print(f"CLASS NAME {class_name} not found.")
        return
    
    for elem in classToMethods[class_name]:
        if list(elem.keys())[0] == var_name:
            return elem[var_name]

    print(f"VARIABLE NAME {var_name} not found.")

    

def interpretMethod(class_name, method_name, arguments: list):
    if class_name not in classToMethods:
        print(f"CLASS NAME {class_name} not found.")
        return
    
    for m in classToMethods[class_name]:
        if list(m.keys())[0] == method_name:
            # print( list(m.values())[0] )
            return interpretBytecode(list(m.values())[0], memory=dict(enumerate(arguments)))

    print(f"METHOD NAME {method_name} not found.")

def interpretBytecode(byteArray, index=0, stack=[], memory={}):
    byteObj = byteArray[index]
    # print(byteObj, '\n')
    match byteObj["opr"]:
        case "return":
            # print("return")
            if byteObj["type"] is None:
                return None
            assert (len(stack) > 0)
            return stack.pop()

        case "push":
            # print("push")
            stack.append(byteObj["value"]["value"])
            # print(stack)

        case "load":
            # print(byteObj)
            # stack.append(memory[byteObj["index"]])
            match byteObj["type"]:
                case "ref" | "int" :
                    stack.append(memory[byteObj["index"]])
                    # stack.append([])
                    # print(stack)
                # case "int":
                #    stack.append(memory[byteObj["index"]])
            # print(memory)

        case "binary":
            a = stack.pop()
            b = stack.pop()
            match byteObj["operant"]:
                case "add":
                    stack.append(a+b)
                case "mul":
                    stack.append(a*b)
                case "sub":
                    stack.append(a-b)
                case _:
                    print("operant", byteObj["condition"], "not implemented")
                    return

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
                case "lt":
                    jump = b < a
                case _:
                    print("condition", byteObj["condition"], "not implemented")
                    return

            if jump:
                return interpretBytecode(byteArray, byteObj["target"], stack, memory)

        case "ifz":
            assert (len(stack) >= 1)
            elem = stack.pop()
            jump = False

            match byteObj["condition"]:
                case "le":
                    jump = elem is None or elem <= 0
                case "ne":
                    jump = elem is not None and elem != 0
                case _:
                    print("condition", byteObj["condition"], "not implemented")
                    return
            # print("jump:", jump)
            # print(byteObj)
            if jump:
                # print(byteObj)
                return interpretBytecode(byteArray, byteObj["target"], stack, memory)

        case "store":
            memory[byteObj["index"]] = stack.pop()
        case "new":
            pass
            # print(byteObj["opr"] + " not implemented")
            # return
        case "put":
            print(byteObj["opr"] + " not implemented")
            return
        case "invoke":
            to_invoke = byteObj["method"]

            # print(stack)

            num_args = len(to_invoke["args"])
            args = stack[-num_args:]
            stack = stack[:-num_args]

            res = interpretMethod(
                to_invoke["ref"]["name"], to_invoke["name"], dict(enumerate(args)))
            stack.append(res)

        case "incr":
            memory[byteObj["index"]] += byteObj["amount"]
            stack.append(memory[byteObj["index"]])
        case "goto":
            # print(byteArray)
            # print( byteObj["target"], '\n')
            return interpretBytecode(byteArray, byteObj["target"], stack, memory)
        case "array_load":
            index_array = stack.pop()
            array = stack.pop()

            if index_array > len(array):
                raise RuntimeError("Out of bounds.")

            stack.append(array[index_array])

        case "array_store":
            # print(stack)
            elem = stack.pop()
            index_array = stack.pop()
            array = stack.pop()
            array.append(elem)
            stack.append(array)

        case "get":
            value = getVarValue( byteObj["field"]["class"], byteObj["field"]["name"] )
            stack.append( value )
        
        case "newarray":
            # stack.append([[], byteObj["dim"]]) # list 2 elements: (array, size)
            stack.append([]) # list 2 elements: (array, size)
        
        case "dup":
            if byteObj["words"] != 1:
                print(byteObj["opr"] + " not implemented (for words > 1)")
            # stack.append( stack[-1] )

        case "arraylength":
            stack.append( len(stack[-1]) )

        case "throw":
            raise RuntimeError("Throwing an exception (incomplete)")
        
        case _:
            print(byteObj["opr"] + " not implemented")
            return

    # print(byteArray)
    if (len(byteArray) > index):
        return interpretBytecode(byteArray, index+1, stack, memory)
    else:
        return "something"


def interpretProjDir(proj_directory: str):
    print(proj_directory)
    for file in glob.iglob(proj_directory + "/**/*.class", recursive=True):
        new_filename = "." + file.split('.')[1] + ".json"
        # print(new_filename)
        # ret = subprocess.run(["jvm2json", "-s", file, "-t", new_filename ])

        # if "Calls.json" not in new_filename:
        #     continue

        f = open(new_filename)
        data: json = json.load(f)
        saveClassMethods(data)
        #print(classToMethods)
        f.close()
        #return data

interpretProjDir(os.path.join(".", "assignment-3", "classes"))
