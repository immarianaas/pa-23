import os
from tree_sitter import Language, Parser

LANGUAGE_FILE = "./languages.so" # the ./ is important
PATH_TO_TREE_SITTER_JAVA = "tree-sitter-java"
Language.build_library(LANGUAGE_FILE, [PATH_TO_TREE_SITTER_JAVA])

# Initialize the Tree-sitter parser with the Java grammar
parser = Parser()
parser.set_language(Language(LANGUAGE_FILE, "java"))


## Define a function to find class dependencies, including imports, arguments, and return types
def find_class_dependencies(node, dependencies=set()):
    for child in node.children:
        if child.type == 'import_declaration':
            import_node = child.child_by_field_name('import_clause')
            if import_node is not None:
                import_path = import_node.string.strip().replace("import ", "")
                dependencies.add(import_path)

        elif child.type == 'class_declaration':
            identifier_node = child.child_by_field_name('identifier')
            if identifier_node is not None:
                class_name = identifier_node.string
                dependencies.add(class_name)

            # Check for method dependencies
            for method_child in child.children:
                if method_child.type == 'method_declaration':
                    # Method return type
                    method_return_type_node = method_child.child_by_field_name('type')
                    if method_return_type_node is not None:
                        method_return_type = method_return_type_node.string.strip()
                        dependencies.add(method_return_type)

                    # Method arguments
                    for param_child in method_child.children:
                        if param_child.type == 'formal_parameter':
                            param_type_node = param_child.child_by_field_name('type')
                            if param_type_node is not None:
                                param_type = param_type_node.string.strip()
                                dependencies.add(param_type)

        find_class_dependencies(child, dependencies)


# Define a recursive function to analyze Java code from files
def analyze_java_code_from_file(file_path, dependencies=set()):
    with open(file_path, 'r') as java_file:
        java_code = java_file.read()

    # Parse the Java code
    tree = parser.parse(bytes(java_code, 'utf8'))
    find_class_dependencies(tree.root_node, dependencies)

# Define a function to print the AST
def print_ast(node, depth=0):
    indent = '  ' * depth
    print(f"{indent}{node.type}")

    for child in node.children:
        print_ast(child, depth + 1)

# Directory containing your Java files
java_files_directory = 'pa-23/course-02242-examples/src/dependencies/java/dtu/deps/'

# Initialize a set to store class dependencies
all_dependencies = set()

# Recursively analyze Java files in the directory
def analyze_java_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                print(f"Analyzing {file_path}:")
                analyze_java_code_from_file(file_path, all_dependencies)

# Start the analysis
analyze_java_files(java_files_directory)

# Print the class dependencies
print("Class Dependencies:")
for dependency in all_dependencies:
    print(dependency)

# Print the AST of the first file for debugging
if all_dependencies:
    first_file_path = os.path.join(java_files_directory, os.listdir(java_files_directory)[0])
    with open(first_file_path, 'r') as first_java_file:
        first_java_code = first_java_file.read()
    first_tree = parser.parse(bytes(first_java_code, 'utf8'))
    print("\nAbstract Syntax Tree (AST) of the first file:")
    print_ast(first_tree.root_node)
