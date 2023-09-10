from tree_sitter import Language, Parser
import os
import pprint 
import glob


FILE = "./../java.so" # the ./ is important
Language.build_library(FILE, ["tree-sitter-java"])
JAVA_LANGUAGE = Language(FILE, "java")
parser = Parser()
parser.set_language(JAVA_LANGUAGE)

pp = pprint.PrettyPrinter(indent=4)

# -----------------------------------------------------------------------------------------------------------------------
#                                 HELPER FUNCTIONS TO MERGE PACKAGES AND CLASSES, ETC
# -----------------------------------------------------------------------------------------------------------------------


lookup_table = {
    "String": "java.lang.String",
    "Integer": "java.lang.Integer",
    "System": "java.lang.System"
}

def is_complete_class( c ):
    return len( c.split('.') ) > 1

def is_asterisk_class( c ):
    return len( c.split('.') ) > 1 and c[-1] == '*'

def is_short_class( c ):
    return len( c.split('.') ) == 1

def complete_dict( dict ):
    # complete single classes
    all_classes = list( dict.keys() ) + [ elem for l in dict.values() for elem in l ]
    total_complete_classes = [ elem for elem in all_classes if is_complete_class( elem ) and not is_asterisk_class(elem) ]

    new_dict = {}
    for k, v in dict.items():
        list_complete_classes = list( filter( is_complete_class, v ) ) + [k]
        complete_classes_short = set( [ elem.split('.')[-1] for elem in list_complete_classes ] )
        short_classes = set( filter( is_short_class, v ) )

        missing_package = short_classes - complete_classes_short
        # print( "in the same package (missing package):", missing_package )

        package = k.rsplit('.', 1 )[0]
        #list_complete_classes += [ package + "." + sc for sc in missing_package ]
        # def find_package( short_class, package, asterisk_classes, total_complete_classes ):
        asterisk_classes = [ elem for elem in list_complete_classes if elem[-1] == '*']

        list_complete_classes += [ find_package( sc, package, asterisk_classes, total_complete_classes) for sc in missing_package ]
        list_complete_classes = [elem for elem in list_complete_classes if not is_asterisk_class( elem )]

        new_dict[k] = [elem for elem in list_complete_classes if elem != k ]


    # del new_dict[ "dtu.deps.normal.Primes implements Iterable<Integer>" ]

    # complete single classes
    all_classes = list( dict.keys() ) + [ elem for l in dict.values() for elem in l ]
    total_complete_classes = [ elem for elem in all_classes if len( elem.split('.') ) > 1 and elem[-1] != '*' ]

    return new_dict

def find_package( short_class, package, asterisk_classes, total_complete_classes ):
    global lookup_table

    if package + "." + short_class in total_complete_classes:
        return package + "." + short_class
    
    for ac in asterisk_classes:
        possible_class = ac[:-1] + short_class
        if possible_class in total_complete_classes:
            return possible_class
    
    if short_class in lookup_table:
        return lookup_table[short_class]
        
    return "WILL BE IGNORED: " + short_class
    # return ''

# -----------------------------------------------------------------------------------------------------------------------
#                                                     "REAL" PROGRAM STARTS HERE
# -----------------------------------------------------------------------------------------------------------------------

# base class for visiting
class SyntaxFold:

    def visit( self, node ):
        results = [ self.visit( n ) for n in node.children ]

        if hasattr( self, node.type ):
            return getattr(self, node.type)(node, results)
        
        return self.default(node, results)

    def default(self, node, results):
        return set().union(*results)
    
# get the main class name of the file
class ClassName( SyntaxFold ):
        
    def class_declaration(self, node, results):
        if node.parent.type != 'program':
            return set()
        

        names = node.children_by_field_name('name')
        return { name.text for name in names }

    def class_body( self,node, results ):
        return set()
    
# get the classes imported with import statements
class DirectImports( SyntaxFold ):

    def import_declaration( self, node, results):
        ret = []
        for c in node.children:
            ret += list( self.visit(c) )
            if c.text == b'*':
                ret[-1] += b'.*'

        return ret

    def scoped_identifier( self, node, results):
        return { node.text }
    
    def class_body( self, node, results ):
        return set()
    
    def package_declaration( self, node, results):
        return set()
    
# get the package name of the current file
class PackageName( SyntaxFold ):
    def package_declaration( self, node, results):
        ret = [ c.text for c in node.children if c.type == 'scoped_identifier']
        return set(ret)
    
# get the classes of declared/instantiated objects
class ObjectTypes( SyntaxFold ):

    def type_identifier( self, node, results ):
        if node.parent.type not in [
            'field_declaration',
            'object_creation_expression',
            'local_variable_declaration'
        ]:
            return set()
        
        return { node.text }
    
# get the classes of which static functions are called
class StaticFunctionClasses( SyntaxFold ):

    _variables = []

    def visit( self, node):
        self._variables.clear()
        candidates = super().visit(node)
        return candidates - set( self._variables )
    
    def field_access(self, node, results):
        object = node.children_by_field_name('object')
        return set([o.text for o in object])

    def variable_declarator( self, node, results):
        vars = node.children_by_field_name('name')
        self._variables += [ v.text for v in vars ]
        return set()

class ArgumentTypes( SyntaxFold ):
    def formal_parameter( self, node, results):
        res = []
        for c in node.children_by_field_name('type'):
            if c.type == 'array_type':
                res += [ elem.text for elem in c.children_by_field_name('element') ]
            else:
                res += [ c.text ]
        return set(res)
    
class ReturnTypes( SyntaxFold ):
    def method_declaration( self, node, results ):

        res = []
        for c in node.children_by_field_name('type'):
            if c.type == 'generic_type':
                self.visit( c )
            else:
                res += [ c.text ]
        return set(res)
    
    def generic_type(self, node, results):
        res = []
        for c in node.children:
            res += list(self.visit( c ))
        return set(res)

    def type_identifier( self, node, results ):
        if node.parent.type not in ['generic_type', 'type_arguments'] :
            return set()
        return { node.text }
    
    def type_arguments( self, node, results ):
        res = []
        for c in node.children:
            res += list( self.visit( c ) )
        return set(res)
    

dict = {}

proj_path = "../course-02242-examples"
for file in glob.iglob(proj_path+"/**/*.java", recursive=True):
    with open(file, "rb") as f:

        tree = parser.parse(f.read())

        print()

        package_name = PackageName().visit( tree.root_node )
        class_name = ClassName().visit( tree.root_node ) 

        assert( len(package_name) == 1 )
        assert( len(class_name) == 1 )

        main_class = (package_name.pop() + b'.' + class_name.pop() ).decode()

        direct_imports = DirectImports().visit( tree.root_node )
        object_types = ObjectTypes().visit( tree.root_node )
        static_function_class = StaticFunctionClasses().visit( tree.root_node )
        argument_types = ArgumentTypes().visit( tree.root_node )
        return_types = ReturnTypes().visit( tree.root_node )

        dict[ main_class] = list(direct_imports) + list(object_types) + list( static_function_class ) + list( argument_types ) + list( return_types )
        dict[ main_class] = [ elem.decode() for elem in dict[main_class]]


new_dict = complete_dict( dict )
pp.pprint(new_dict)
