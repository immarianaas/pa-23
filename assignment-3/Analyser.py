import os
from CreateGraph import CreateGraph
import json


dict = {}


def createDictEntry(className):
    dict[className] = {
        "relationships": {
            "Dependency": [],
            "Association": [],
            "Aggregation": [],
            "Composition": [],
            "Realization": [],
            "Inheritance": [],
        },
        "fields": {
            "Public": {"name": "", "type": "", "val": ""},
            "Private": {"name": "", "type": "", "val": ""},
            "Protected": {"name": "", "type": "", "val": ""},
            "Package": {"name": "", "type": "", "val": ""},
        },
        "functions": {
            "Public": {"name": "", "arg": {}, "return": ""},
            "Private": {"name": "", "arg": {}, "return": ""},
            "Protected": {"name": "", "arg": {}, "return": ""},
            "Package": {"name": "", "arg": {}, "return": ""},
        },
    }


def JsonToDictEntries(data: json):
    classname = data["name"]

    createDictEntry(classname)

    print(data)


def JsonDirectoryToDict(json_directory):
    for file in os.listdir(json_directory):
        f = open(json_directory + "\\" + file)
        data: json = json.load(f)
        f.close()
        JsonToDictEntries(data)


JsonDirectoryToDict("assignment-3\Json bytecode")
print(json.dumps(dict, indent=4))
