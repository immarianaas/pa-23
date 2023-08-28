import os
import re
path = "./course-02242-examples/src/dependencies/java/dtu/deps/simple/"


# { principal class : [ immediate dependencies ] }
dict = {}

for file in os.listdir( path ):
    with open(path + file) as f:

        src_code = f.read()

        no_comment = re.sub( "/\*(?:[^*]|\*(?!/s))*\*/", "", src_code)
        no_comment = re.sub( "//.*\n", "", no_comment)

        # print(src_code)
        # print("no commentt" + no_comment)
         

        package = re.findall(r"(?<=package ).*(?=;)", no_comment )
        class_name = re.findall(r"(?<=class ).*(?= )", no_comment )

        direct_imports = re.findall(r"(?<=import ).*(?=;)", no_comment )

        objects_created = re.findall(r"(?<=new ).*(?=\()", no_comment )

        print("filename:", file,
              "\t| class name: ", package + class_name, 
              "\t| direct imports: ", direct_imports,
              "\t| objects created: ", objects_created )
        

        main_class = package[0] + "." if package != [] else ""
        main_class += class_name[0]

        dict[ main_class ] = direct_imports + objects_created


print()
print( dict )
        

