from CreateGraph import CreateGraph
import json

dict = {}

f = open("assignment-3\Json bytecode\primes.json")


data: json = json.load(f)
f.close()

classname = data["name"]


def createDictEntry(className):
    dict[className] = {
        "relationships": {
            "Dependency": {},
            "Association": {},
            "Aggregation": {},
            "Composition": {},
            "Implementation": {},
            "Inheritance": {},
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


realizations = []

for i in data["interfaces"]:
    print(i)


CreateGraph({})
