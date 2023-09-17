import re
import graphviz

def CreateGraph(dict):
    s = graphviz.Digraph("structs", node_attr={"shape": "record"})
    field_diagram = ""
    function_diagram = ""
    main_string = ""
    for key, value in dict.items():
        # print(key, value)
        field_diagram = ""
        if value["fields"] != []:
            for val in value["fields"]:
                for key1, value1 in val.items():
                    if key1 == "name": field_diagram += value1 + " : "
                    elif key1 == "access":
                        value_joined="[]"
                        if len(value1) >= 1: value_joined = ' '.join(str(e) for e in value1)
                        field_diagram += value_joined + " | "
        
        function_diagram = ""
        if value["functions"] != []:
            for fun in value["functions"]:
                for key2, value2 in fun.items():
                    if key2 == "name":
                        if value2 == "<init>": function_diagram += "init"
                        if value2 =="<clinit>": function_diagram += "clinit"
                        else: function_diagram += value2
                    elif key2 == "arguments":
                        value_joined="()"
                        if len(value2) >=1: value_joined = "(" + ' '.join(str(e) for e in value2) + ")"
                        function_diagram +=  value_joined + ": " 
                    elif key2 == "returns":
                        if type(None) == type(value2): function_diagram += "null" + " | "
                        else: function_diagram += value2 + " | "

        
        if field_diagram: main_string = field_diagram
        if function_diagram: main_string += function_diagram
        # print(main_string[:-2], '\n')


        if field_diagram: s.node(key, r"{ " + key + " | " + main_string[:-2] + "}",)

        
        for val in value["relations"]["Composition"]:
            s.edge(key, val, arrowhead="diamond")
        for val in value["relations"]["Realization"]:
            s.edge(key, val, arrowhead="normalo", style="dashed")
        for val in value["relations"]["Inheritance"]:
            s.edge(key, val, arrowhead="normalo")
        for val in value["relations"]["Aggregation"]:
            s.edge(key, val, arrowhead="diamondo")
        for val in value["relations"]["Dependency"]:
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

    s.render("./class-graph/class-diagram-3.gv").replace("\\", "/")

