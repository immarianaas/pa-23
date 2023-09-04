from tree_sitter import Language, Parser
FILE = "./../java.so" # the ./ is important
Language.build_library(FILE, ["./../tree-sitter-java"])
JAVA_LANGUAGE = Language(FILE, "java")
parser = Parser()
parser.set_language(JAVA_LANGUAGE)

example_path = "../example-dependency-graphs/src/main/java/dtu/compute/simple/Example.java"

with open(example_path, "rb") as f:
    tree = parser.parse(f.read())
# the tree is now ready for analysing
print(tree.root_node.sexp())



class SyntaxFold:

    def visit( self, node ):
        results = [ self.visit( n ) for n in node.children ]

        if hasattr( self, node.type ):
            return getattr(self, node.type)(node, results)
        
        return self.default(node, results)
    
    # def default(self, node, results): # TODO: we prob dont need these 'results'
    #     print("DEFAULT:", node )

    
class Printer( SyntaxFold ):
    def default(self,node, results):
        print(node)
        print(results)

class TypeIdentifiers( SyntaxFold ):
    def default(self, node, results):
        return set().union(*results)
    
    def type_identifier(self, node, results):
        return { b"a: " + node.text }
    
    def scoped_identifier( self, node, results):
        return { b"b: " + node.text }
    
    def package_declaration( self, node, results ):
        return { b"c: " + node.text }

# Printer().visit( tree.root_node )

print()
print( TypeIdentifiers().visit( tree.root_node ) )