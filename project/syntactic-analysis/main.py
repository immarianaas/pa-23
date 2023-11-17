import os
from tree_sitter import Language, Parser
import glob
import sys

from syntax_fold import *
from printing_utils import *
from complete_utils import *

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
    DATA += get_java_types()

    for file in glob.iglob(PROJ_PATH + "/**/*.java", recursive=True):
        if "EntryPoint.java" in file or "AppTest.java" in file:
            continue


        with open(file, "rb") as f:
            tree = parser.parse(f.read())


            package_name = PackageName().visit(tree.root_node).pop().decode()
            
            class_name = ClassName( package_name )
            class_name.visit(tree.root_node)
            class_repr = class_name.class_repr

            # assert len(package_name) == 1
            print(file)

            # print( package_name )
            # print( class_name )

            # functions = FunctionsName

            aaa = FunctionFunctions(class_repr)
            help = aaa.visit(tree.root_node)

            print("*************************")
            print( aaa.class_repr.methods) 
            print("*************************")

            # print(help)
            # print("RESULT:", aaa.data)

            # DATA[ get_overal_class_name(class_name.data, package_name) ] = aaa.data
            #DATA[ class_repr ] = aaa.data
            
            DATA.append( aaa.class_repr )

            # break

    




if __name__ == "__main__":
    main()

    #print_data( DATA )

    #print(DATA)

    print("----------------------------------------------------------------------------------------------------------------------")


    complete( DATA )

    print("----------------------------------------------------------------------------------------------------------------------")

    print_data( DATA )

    print("----------------------------------------------------------------------------------------------------------------------")

    get_tuples( DATA, "dk.dtu.pa.geometry.ResizeShapes", "resize")
    get_tuples( DATA, "dk.dtu.pa.App", "main")
