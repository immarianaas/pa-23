import re
import graphviz


def CreateGraph(dict):
    s = graphviz.Digraph("structs", node_attr={"shape": "record"})

    for key, value in dict.items():
        s.node(key, re.sub("<.*>", "", key))
        for val in value["composition"]:
            s.edge(key, val, arrowhead="diamond")
        for val in value["realization"]:
            s.edge(key, val, arrowhead="normalo", style="dashed")
        for val in value["inheritance"]:
            s.edge(key, val, arrowhead="normalo")
        for val in value["aggregation"]:
            s.edge(key, val, arrowhead="diamondo")
        for val in value["dependency"]:
            s.edge(key, val, arrowhead="vee", style="dashed")

    s.node("a", "", color="white")
    s.node("b", "", color="white")
    s.node("c", "", color="white")
    s.node("d", "", color="white")
    s.node("e", "", color="white")
    s.node("f", "", color="white")

    s.edge("a", "b", arrowhead="diamond", label="composition")
    s.edge("b", "c", arrowhead="normalo", style="dashed", label="realization")
    s.edge("c", "d", arrowhead="normalo", label="inheritance")
    s.edge("d", "e", arrowhead="diamondo", label="aggregation")
    s.edge("e", "f", arrowhead="vee", style="dashed", label="dependency")

    s.render("assignment-2/classs-graph/class-diagram.gv").replace("\\", "/")
