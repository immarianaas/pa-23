import os
from CreateGraph import CreateGraph
import json
import glob
import subprocess

dict = {}


def createDictEntry(className: str):
    if (className not in dict.keys()) & (
        className
        not in [
            "byte",
            "short",
            "int",
            "long",
            "float",
            "double",
            "boolean",
            "char",
        ]
    ):
        dict[className] = {
            "relations": {
                "Dependency": [],
                "Association": [],
                "Aggregation": [],
                "Composition": [],
                "Realization": [],
                "Inheritance": [],
            },
            "fields": [],
            "functions": [],
        }
        return True
    return False # if it is a basic type


def JsonToDictEntries(data: json):
    classname = data["name"]

    createDictEntry(classname)

    GetInterfaces(data, classname)
    GetFields(data, classname)

    GetMethods(data, classname)
    GetInnerClasses( data, classname )

def GetFields(data, classname):
    fields = data["fields"]
    for f in fields:
        dict[classname]["fields"].append({"name": f["name"], "access": f["access"]})
        # TODO: "kind" in f["type"] and
        #       i added this but i haven't analysed its implications
        if "kind" in f["type"] and f["type"]["kind"] == "class":
            createDictEntry(f["type"]["name"])
            dict[classname]["relations"]["Aggregation"].append(f["type"]["name"])

def GetInterfaces(data: json, classname: str):
    interfaces = data["interfaces"]
    for i in interfaces:
        i_name = i["name"]
        dict[classname]["relations"]["Realization"].append(i_name)
        createDictEntry(i_name)
        for arg in i["args"]:
            if arg["type"]["kind"] == "class":
                createDictEntry(i_name)
                dict[i_name]["relations"]["Dependency"].append(arg["type"]["name"])

def GetMethods(data: json, classname: str):
    methods = data["methods"]
    for i in methods:
        dict[classname]["functions"].append( getMethodInfo(i, classname) )

def getType( obj: json ):
    assert( "type" in obj )
    if obj["type"] is None:
        return None

    if "base" in obj["type"]:
        return obj["type"]["base"] 
    
    if "name" in obj["type"] and obj["type"]["kind"] != "typevar":
        return obj["type"]["name"]

    # not a good way to do this:
    if obj["type"]["kind"] == "array" and "name" in obj["type"]["type"]:
        return obj["type"]["type"]["name"] + "[]"

    return None

def getMethodInfo(method: json, classname: str):
    info = {}

    info["name"] = method["name"]
    info["access"] = method["access"]

    arguments = method["params"]
    info["arguments"] = [ getType( elem ) for elem in method["params"] if getType( elem ) is not None]
    
    info["returns"] = getType( method["returns"] )

    

    
    returns_obj_name = info["returns"]
    if returns_obj_name is not None:
        if createDictEntry(returns_obj_name):
            dict[classname]["relations"]["Dependency"].append(returns_obj_name)


    for elem in info["arguments"]:
        if elem[-2:] == "[]":
            elem = elem[:-2]

        # create entry for this new element, if it is new
        if createDictEntry(elem):
            # create dependency from this element, to the argument
            dict[classname]["relations"]["Dependency"].append(elem)


    # print( info )
    return info

def GetInnerClasses(data: json, classname: str):
    for inner_class in data["innerclasses"]:
        inner_class_name = inner_class["class"]
        if inner_class["outer"] == classname:
            dict[classname]["relations"]["Composition"].append( inner_class_name )
            createDictEntry(inner_class_name)

def ProjDirectoryToDict(proj_directory: str):
    for file in glob.iglob(proj_directory + "/**/*.class", recursive=True):
        new_filename = "." + file.split('.')[1] + ".json"
        # ret = subprocess.run(["jvm2json", "-s", file, "-t", new_filename ])

        f = open( new_filename )
        data: json = json.load(f)
        f.close()
        JsonToDictEntries(data)


ProjDirectoryToDict(os.path.join("./","classes"))
print(json.dumps(dict, indent=4))
CreateGraph(dict)