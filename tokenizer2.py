import os
import re
path = "./course-02242-examples/src/dependencies/java/dtu/deps/simple/"

for file in os.listdir( path ):
    with open(path + file) as f:

        src_code = f.read()

        no_comment = re.sub( "/\*(?:[^*]|\*(?!/s))*\*/", "", src_code)
        no_comment = re.sub( "//.*\n", "", src_code)

        print(src_code)
        print("no commentt \n #####################\n" + no_comment + "\n ############")
         

        class_name = re.search("class\s\w*", no_comment )
        print("class name: ", class_name)