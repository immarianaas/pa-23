from tree_sitter import Language, Parser
import os
import pprint 
import glob
import re


# -----------------------------------------------------------------------------------------------------------------------
#                                 HELPER FUNCTIONS TO MERGE PACKAGES AND CLASSES, ETC
# -----------------------------------------------------------------------------------------------------------------------


lookup_table = {
    "String": "java.lang.String",
    "Integer": "java.lang.Integer",
    "System": "java.lang.System"
}

primitiva_java_types = {
    "int",
    "byte",
    "short",
    "long",
    "float",
    "double",
    "boolean",
    "char",
    "void"
}


def clean_brackets( dict ):
    new_dict = {}

    sub = lambda x : re.sub("<.*>", "", x)

    for k, v in dict.items():
        
        new_value = {}
        for kk, vv in v.items():
            new_value[kk] = [ sub(elem) for elem in vv ]
        
        new_dict[sub(k)] = new_value
    
    return new_dict



def complete_dict_short( dict ):
    new_dict = {}

    get_small = lambda x : re.sub("<.*>", "", x).split('.')[-1]

    for k, v in dict.items():
        new_dict[ get_small(k) ] = list({ get_small(elem) for elem in v if elem not in primitiva_java_types and get_small(elem) != '*' and get_small(elem) != get_small(k)})

    return new_dict
        
def add_dependencies( dep_dict, full_dict ):
    new_dict = {}

    for k, v in full_dict.items():

        if k not in dep_dict:
            continue

        deps = set( dep_dict[k] )
        all_others = set( v["composition"] + v["realization"] + v["inheritance"] + v["aggregation"] )

        new_dict[k] = v.copy()
        new_dict[k]["dependency"] = list( deps - all_others )

    return new_dict





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

        #field = node.children_by_field_name('field')
        #print( [a.text for a in field])

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
    


def get_dependencies():

    FILE = "./../java.so" # the ./ is important
    Language.build_library(FILE, ["tree-sitter-java"])
    JAVA_LANGUAGE = Language(FILE, "java")
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)

    pp = pprint.PrettyPrinter(indent=4)


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


    new_dict = complete_dict_short( dict )
    # pp.pprint(new_dict)
    return new_dict



# get_dependencies()