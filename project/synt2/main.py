import os
from tree_sitter import Language, Parser
import glob
import sys

from syntax_fold import *

this_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(this_path)


LANGUAGE_FILE = this_path+"/java.so" # the ./ is important
#PATH_TO_TREE_SITTER_JAVA = "tree-sitter-java"
PATH_TO_TREE_SITTER_JAVA = this_path+"/tree-sitter-java"
Language.build_library(LANGUAGE_FILE, [PATH_TO_TREE_SITTER_JAVA])

# Initialize the Tree-sitter parser with the Java grammar
parser = Parser()
parser.set_language(Language(LANGUAGE_FILE, "java"))

# PROJ_PATH = "../../course-02242-examples" # JAVA PROJECT TO ANALYSE
PROJ_PATH = "../pa-app" # JAVA PROJECT TO ANALYSE

DATA = []

def main():
    global DATA
    # DATA += get_java_types()

    for file in glob.iglob(PROJ_PATH + "/**/*.java", recursive=True):
        if "EntryPoint.java" in file or "AppTest.java" in file:
            continue


        with open(file, "rb") as f:
            tree = parser.parse(f.read())

            class_info = ClassInfo()
            class_info.visit(tree.root_node)

            class_repr = ClassRepr(class_info.class_name, class_info.class_package, class_info.class_type, methods=[])

            # this `class_info.methods` doesn't have a ClassRepr in the "methods"
            for m in class_info.methods:
                m.related_class = class_repr
                m.invocations = list(set(m.invocations))
                class_repr.methods.append( m )

            class_repr.methods = list(set(class_repr.methods))

            DATA.append( class_repr )

def find_method_from_temp_in_class(temp_method: TempMethodRepr, related_class: ClassRepr):
    for m in related_class.methods:
        if temp_method.method_name == m.name:
            if ( temp_method.parameters == m.parameter_types ):
                return m
            print("here", temp_method.parameters, m.parameter_types)
            print("--> searching for method", temp_method)
        
            
def find_method_from_temp(DATA, method: TempMethodRepr, this_class: ClassRepr):
    if method.related_class.specific_name == "<this>":
        return find_method_from_temp_in_class(method, this_class)
    
    for c in DATA:
        if method.related_class.specific_name == c.class_name:
            return find_method_from_temp_in_class(method, c)
        
def find_class_from_temp(DATA, temp_class: TempClassRepr):
    for c in DATA:
        if c.name == temp_class.specific_name:
            return c
    assert False
    
def resolve_temp_methods(DATA):
    for c in DATA:
        for m in c.methods:
            true_invocations = []
            for m_inv in m.invocations:
                true_m_inv = find_method_from_temp(DATA, m_inv, c)
                assert true_m_inv is not None
                true_invocations.append( true_m_inv )
            
            m.invocations = true_invocations
            

def resolve_return_types(DATA):
    for c in DATA:
        for m in c.methods:
            if m.return_type == "<this>":
                m.return_type = c


def get_starting_method(DATA, class_name: str, func_name: str):
    for c in DATA:
        # comparing full name here
        if c.get_name() == class_name:
            for m in c.methods:
                if m.name == func_name:
                    return m
                
def get_tuples(DATA, class_name: str, func_name: str):
    starting_m = get_starting_method(DATA, class_name, func_name)
    assert starting_m is not None

    print_tuples_from_method(starting_m)



def print_tuples_from_method(method: MethodRepr):
    for inv in method.invocations:
        print(f"({method.print_full()} , {inv.print_full()})")
        print_tuples_from_method(inv)
        


main()
resolve_temp_methods(DATA)
resolve_return_types(DATA)
print("-------"*3)

for c in DATA:
    c.pprint()


get_tuples( DATA, "dk.dtu.pa.App", "appMain")

