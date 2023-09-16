import os
from CreateGraph import CreateGraph
import json


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


def JsonToDictEntries(data: json):
    classname = data["name"]

    createDictEntry(classname)

    GetInterfaces(data, classname)
    GetFields(data, classname)


def GetFields(data, classname):
    fields = data["fields"]
    for f in fields:
        dict[classname]["fields"].append({"name": f["name"], "access": f["access"]})
        if f["type"]["kind"] == "class":
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


def JsonDirectoryToDict(json_directory: str):
    for file in os.listdir(json_directory):
        f = open(json_directory + "\\" + file)
        data: json = json.load(f)
        f.close()
        JsonToDictEntries(data)


JsonDirectoryToDict("assignment-3\Json bytecode")
print(json.dumps(dict, indent=4))
