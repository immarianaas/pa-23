import re
import sys
from tree_sitter import Language, Parser
import json
import pprint
import glob
import graphviz
from graphviz import nohtml

from ClassDiagram import *


FILE = "./../java.so"  # the ./ is important
Language.build_library(FILE, ["tree-sitter-java"])
JAVA_LANGUAGE = Language(FILE, "java")
parser = Parser()
parser.set_language(JAVA_LANGUAGE)

pp = pprint.PrettyPrinter(indent=4)

primitiva_java_types = [
    "int",
    "byte",
    "short",
    "long",
    "float",
    "double",
    "boolean",
    "char",
]

dict = {}


# looks for every class decleration node and adds the node with dependencies to the dictionary
def walk_tree(node, outerClass=None):
    for child in node.children:
        if child.type == "class_declaration":
            name = child.child_by_field_name("name").text.decode()

            dict[name] = {
                "composition": [],
                "realization": getInterfaces(child),
                "inheritance": getSuperclasses(child),
                "aggregation": getfields(child),
            }

            if outerClass != None:
                dict[outerClass]["composition"].append(name)

            walk_tree(child, name)
        else:
            walk_tree(child, outerClass)


def getfields(child):
    body = child.child_by_field_name("body")

    fields = []
    for child in body.children:
        if child.type == "field_declaration":
            fieldValue = child.child_by_field_name("declarator").child_by_field_name(
                "value"
            )
            if (
                fieldValue is not None
                and fieldValue.child_by_field_name("type") is not None
            ):
                field_type = fieldValue.child_by_field_name("type").text.decode()
                if field_type not in primitiva_java_types:
                    fields.append(field_type)
                    if field_type not in dict.keys():
                        dict[field_type] = {
                            "composition": [],
                            "realization": [],
                            "inheritance": [],
                            "aggregation": [],
                        }
    return fields


def getSuperclasses(child):
    superclasses = child.child_by_field_name("superclass")
    extends_class = []
    if superclasses is not None:
        for superclass in superclasses.children:
            if superclass.type == "type_identifier":
                extends_class.append(superclass.text.decode())
                if extends_class.text.decode() not in dict.keys():
                    dict[extends_class.text.decode()] = {
                        "composition": [],
                        "realization": [],
                        "inheritance": [],
                        "aggregation": [],
                    }
    return extends_class


def getInterfaces(child):
    interfaces = child.child_by_field_name("interfaces")
    implements_interfaces = []
    if interfaces is not None:
        for interface in interfaces.children:
            if interface.type == "type_list":
                implements_interfaces.append(interface.text.decode())
                if interface.text.decode() not in dict.keys():
                    dict[interface.text.decode()] = {
                        "composition": [],
                        "realization": [],
                        "inheritance": [],
                        "aggregation": [],
                    }
    return implements_interfaces


proj_path = "../course-02242-examples"
for file in glob.iglob(proj_path + "/**/*.java", recursive=True):
    with open(file, "rb") as f:
        tree = parser.parse(f.read())

        walk_tree(tree.root_node)


# print(json.dumps(dict, indent=4))

dict = clean_brackets( dict )
dep_dict = get_dependencies()

final_dict = add_dependencies( dep_dict, dict )

print(json.dumps(final_dict, indent=4))

s = graphviz.Digraph("structs", node_attr={"shape": "record"})

dict = final_dict
for key, value in dict.items():
    s.node(key, r"{" + re.sub("<.*>", "", key) + r"|}")
    for val in value["composition"]:
        s.edge(key, val, arrowhead="diamond")
    for val in value["realization"]:
        s.edge(key, val, arrowhead="normalo", style="dashed")
    for val in value["inheritance"]:
        s.edge(key, val, arrowhead="normalo")
    for val in value["aggregation"]:
        s.edge(key, val, arrowhead="diamondo")
    for val in value["dependency"]:
        s.edge(key, val, arrowhead="none")


s.render("assignment-2/classs-graph/class-diagram.gv").replace("\\", "/")
