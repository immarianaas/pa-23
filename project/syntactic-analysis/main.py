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

PROJ_PATH = "../../course-02242-examples" # JAVA PROJECT TO ANALYSE

def main():
    for file in glob.iglob(PROJ_PATH + "/**/*.java", recursive=True):
        with open(file, "rb") as f:
            tree = parser.parse(f.read())


            package_name = PackageName().visit(tree.root_node)
            class_name = ClassName().visit(tree.root_node)

            assert len(package_name) == 1
            assert len(class_name) == 1

            print( package_name )
            print( class_name )



if __name__ == "__main__":
    main()