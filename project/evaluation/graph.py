import graphviz

# first let's read the truth, main function:
truth_list = []
with open("truth-main.txt", "r") as truth:
    for line in truth:
        meth1, meth2 = line[1:-2].split(", ")

        truth_list.append( (meth1, meth2) )


# then let's read the syn, main function:
syn_list = []
with open("syn-main.txt", "r") as truth:
    for line in truth:
        meth1, meth2 = line[1:-2].split(", ")

        syn_list.append( (meth1, meth2) )

# edges = [('a', 'b'), ('a', 'c'), ('a', 'd'), ('c', 'e')]

graph = graphviz.Digraph(engine='fdp')

GREEN = "#90EE90"
RED = "#ffcccb"

# Add edges to the graph
for edge in syn_list:
    if edge in truth_list:
        graph.node(edge[0], color=GREEN, style="filled")
        graph.node(edge[1], color=GREEN, style="filled")
    else:
        graph.node(edge[0], color=RED, style="filled")
        graph.node(edge[1], color=RED, style="filled")
    graph.edge(edge[0], edge[1])

for edge in truth_list:
    if edge in syn_list:
        graph.node(edge[0], color=GREEN)
        graph.node(edge[1], color=GREEN)
    else:
        graph.node(edge[0], color=RED)
        graph.node(edge[1], color=RED)
    graph.edge(edge[0], edge[1])

# Save the graph to a file (e.g., in PNG format)
graph.render(filename='example_graph', format='png', cleanup=True)

# Alternatively, you can view the graph directly
graph.view()
