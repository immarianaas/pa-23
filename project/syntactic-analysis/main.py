import os
from tree_sitter import Language, Parser
import glob

from syntax_fold import *


LANGUAGE_FILE = "./java.so" # the ./ is important
#PATH_TO_TREE_SITTER_JAVA = "tree-sitter-java"
PATH_TO_TREE_SITTER_JAVA = "./tree-sitter-java"
Language.build_library(LANGUAGE_FILE, [PATH_TO_TREE_SITTER_JAVA])

# Initialize the Tree-sitter parser with the Java grammar
parser = Parser()
parser.set_language(Language(LANGUAGE_FILE, "java"))

# PROJ_PATH = "../../course-02242-examples" # JAVA PROJECT TO ANALYSE
PROJ_PATH = "../pa-app" # JAVA PROJECT TO ANALYSE

DATA = {}

def main():
    for file in glob.iglob(PROJ_PATH + "/**/*.java", recursive=True):
        if "EntryPoint.java" in file:
            continue

        with open(file, "rb") as f:
            tree = parser.parse(f.read())


            package_name = PackageName().visit(tree.root_node)
            class_name = ClassName()
            class_name.visit(tree.root_node)

            assert len(package_name) == 1
            print(file)
            assert len(class_name.data.values()) == 1

            # print( package_name )
            # print( class_name )

            # functions = FunctionsName

            aaa = FunctionFunctions("jj")
            help = aaa.visit(tree.root_node)
            # print(help)
            # print("RESULT:", aaa.data)

            DATA[ get_overal_class_name(class_name.data, package_name) ] = aaa.data

            # break

    

def get_overal_class_name(class_name_dict, package_name ):
    if "class" in class_name_dict:
        return f"(c) {package_name.pop().decode()}.{class_name_dict['class'].pop().decode()}"
    
    if "interface" in class_name_dict:
        return f"(i) {package_name.pop().decode()}.{class_name_dict['interface'].pop().decode()}"
    
    if "enum" in class_name_dict:
        return f"(e) {package_name.pop().decode()}.{class_name_dict['enum'].pop().decode()}"
    
    return f"error"

def helper_print_arguments( parameter_set: set ):
    if parameter_set == set():
        return "()"
    
    temp_parameter_set = [ str(elem) for elem in parameter_set ]
    return f"( { '.'.join( temp_parameter_set )} )"
    

    
def print_data():
    for [k, v] in DATA.items():
        print("-"*50)
        print(f"|{'':10s}{k:36s}  |")
        print("-"*50)

        for [func, info_list] in v.items():
            for info in info_list:
                func_str = f"| - {func}{helper_print_arguments(info['parameters'])} : {info['return']}"
                # print( '|'+'-'*(len(func_str)-1) )
                print( '|   '+'-'*(len(func_str)-4) )
                print( func_str )

                

                for [method_name, method_info] in info["function_calls"].items():
                    for method_overload in method_info:
                        print(f"| - - {method_overload['invoking']:30s}...{method_name}{helper_print_arguments(method_overload['parameters'])}")

        print()





if __name__ == "__main__":
    main()

    
    print_data()