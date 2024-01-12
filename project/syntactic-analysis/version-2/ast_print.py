import ast
from graphviz import Digraph

import ast

code = "a = 2 + 3"

tree = ast.parse(code)

# Create a Graphviz Digraph object
dot = Digraph()

# Define a function to recursively add nodes to the Digraph
def add_node(node, parent=None):
    node_name = f"{node.__class__.__name__}"
    
    # Add specific information based on node type
    if isinstance(node, ast.Name):
        node_name += f"\nid={node.id}"
    elif isinstance(node, ast.Constant):
        node_name += f"\nvalue={node.value}"

    dot.node(str(id(node)), node_name)

    # node_name = str(node.__class__.__name__) + str(node.value)
    # dot.node(str(id(node)), node_name)
    if parent:
        dot.edge(str(id(parent)), str(id(node)))
    for child in ast.iter_child_nodes(node):
        add_node(child, node)

# Add nodes to the Digraph
add_node(tree)

# Render the Digraph as a PNG file
dot.format = 'png'
dot.render('my_ast', view=True)