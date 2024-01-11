import graphviz


def createGraph(nodes, edges, dir):
    s = graphviz.Digraph("structs", node_attr={"shape": "record"})
    for n in nodes:
        s.node(n)
    for a in edges:
        s.edge(a[0], a[1])
    s.render(dir + "diagram.gv")
