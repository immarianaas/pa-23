from tree_sitter import Language, Parser
FILE = "./../java.so" # the ./ is important
Language.build_library(FILE, ["./../tree-sitter-java"])
JAVA_LANGUAGE = Language(FILE, "java")
parser = Parser()
parser.set_language(JAVA_LANGUAGE)

example_path = "../course-02242-examples/src/dependencies/java/dtu/deps/normal/Primes.java"

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

    def default(self, node, results):
        return set().union(*results)
    
class Printer( SyntaxFold ):
    def default(self,node, results):
        print(node)
        print(results)



class TypeIdentifiers( SyntaxFold ):
    
    imported = []
    class_name = []
    package_name = []
    
    def import_declaration( self, node, results ):
        ret = []
        for c in node.children:
            ret += [ r for r in self.visit( c ) ]

        self.imported += ret
        return set(ret)
    
    def class_declaration(self, node, results):
        if node.parent.type == 'program':
            a = ClassName().visit( node )
            self.class_name += list( a )

        ret = []
        for c in node.children:
            ret += [ r for r in self.visit( c ) ]

        return set(ret)
        
        #ret = []
        # print( node.text )
        #for c in node.children:
        #    ret += [ r for r in self.visit( c ) ]
        # print( "class_declaration: ", ret )

        # print( dir(node) )
        #return set()
    
    def class_body( self,node, results ):
        return set()

    def identifier(self, node, results ):
        # print("identifyer: ", node.text )
        return { node.text }
    
    def generic_type( self, node, results ):
        # print('generic type: ', node.text)
        return {}
    
    def type_identifier(self, node, results):
        return { b"a: " + node.text }
    
    def scoped_identifier( self, node, results):
        return { b"b: " + node.text }
    
    def package_declaration( self, node, results ):
        ret = [ c.text for c in node.children if c.type == 'scoped_identifier']
        assert ( len(ret) <= 1 )
        self.package_name += ret
        return set()

# Printer().visit( tree.root_node )

class ClassName( SyntaxFold ):
    def class_body( self,node, results ):
        return set()
    
    def identifier(self, node, results ):
        # print("identifyer: ", node.text )
        return { node.text }




print()
print( TypeIdentifiers().visit( tree.root_node ) )


print( "direct imports: ",TypeIdentifiers().imported )
print( "class name: ",TypeIdentifiers().class_name )