import os
import re
path = "./course-02242-examples/src/dependencies/java/dtu/deps/simple/"


# { principal class : [ immediate dependencies ] }
dict = {}

def strip_elems( l ):
    return [ elem.strip() for elem in l]

for file in os.listdir( path ):
    with open(path + file) as f:

        src_code = f.read()

        no_comment = re.sub( "/\*(?:[^*]|\*(?!/s))*\*/", "", src_code)
        no_comment = re.sub( "//.*\n", "", no_comment)

        # print(src_code)
        # print("no commentt" + no_comment)
         

        package = strip_elems( re.findall(r"(?<=package\s)[\s\S]+?(?=;)", no_comment ) )
        class_name = strip_elems( re.findall(r"(?<=class\s)[\s\S]+?(?=\{)", no_comment ))


        direct_imports = strip_elems( re.findall(r"(?<=import\s)[\s\S]+?(?=;)", no_comment ) )
        new_objects = strip_elems( re.findall(r"(?<=new\s)[\s\S]+?(?=\()", no_comment ) )

        print("filename:", file,
              "\t| class name: ", package + class_name, 
              "\t| direct imports: ", direct_imports,
              "\t| objects created: ", new_objects )
        

        main_class = package[0] + "." if package != [] else ""
        main_class += class_name[0]

        dict[ main_class ] = direct_imports + new_objects


print()
print( dict )
        

