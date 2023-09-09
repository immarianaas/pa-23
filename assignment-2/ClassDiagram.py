from tree_sitter import Language, Parser
FILE = "./../java.so" # the ./ is important
Language.build_library(FILE, ["./../tree-sitter-java"])
JAVA_LANGUAGE = Language(FILE, "java")
parser = Parser()
parser.set_language(JAVA_LANGUAGE)

# example_path = "../course-02242-examples/src/dependencies/java/dtu/deps/normal/Primes.java"
example_path = "../course-02242-examples/src/dependencies/java/dtu/deps/simple/Example.java"

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
    types = []

    possible_class_or_object = []
    
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
    
    # def class_body( self,node, results ):
    #     return set()

    def identifier(self, node, results ):
        # print("identifyer: ", node.text )

        if ( node.parent.type == 'method_invocation'):
            print( 'HERE', node.text )
        return { node.text }
    
    def generic_type( self, node, results ):
        # print('generic type: ', node.text)
        return {}
    
    def scoped_identifier( self, node, results):
        return { b"b: " + node.text }
    
    def package_declaration( self, node, results ):
        ret = [ c.text for c in node.children if c.type == 'scoped_identifier']
        assert ( len(ret) <= 1 )
        self.package_name += ret
        return set()
    
    def field_declaration( self, node, results):
        print( node.text)
        return set()
    
    def type_identifier( self, node, results ):
        print( "node.parent.type", node.parent.type)
        if node.parent.type not in [
            'field_declaration',
            'object_creation_expression'
        ]:
            return set()
        
        self.types += [ node.text ]
        return { node.text }
    
    def method_invocation( self, node, results ):

        class_or_object = node.children_by_field_name('object')

        print( "metod", node.text)

        if len(class_or_object) > 0:
            self.possible_class_or_object += list( self.visit(class_or_object[0]) )

        return set()
    
    def field_access(self, node, results):
        print ( "field acess", node.text)

        class_or_object = node.children_by_field_name('object')

        if len(class_or_object) > 0:
            return self.visit(class_or_object[0])


        # return set()

# Printer().visit( tree.root_node )

class ClassName( SyntaxFold ):
    def class_body( self,node, results ):
        return set()
    
    def identifier(self, node, results ):
        # print("identifyer: ", node.text )
        return { node.text }

'''
class Test( SyntaxFold ):
        
    def type_identifier( self, node, results ):
        return {node.text}

print( Test().visit(tree.root_node))
'''

print()
print( TypeIdentifiers().visit( tree.root_node ) )
print()


print( "direct imports: ",TypeIdentifiers().imported )
print( "class name: ",TypeIdentifiers().class_name )
print( "package name: ",TypeIdentifiers().package_name )
print( "types: ",set( TypeIdentifiers().types ))
print( "possible class or object: ", set( TypeIdentifiers().possible_class_or_object ) )

