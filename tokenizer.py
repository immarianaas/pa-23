import os
import re
import pprint 
import graphviz as gv

pp = pprint.PrettyPrinter(indent=4)


path = "./course-02242-examples/src/dependencies/java/dtu/deps/tricky/"
# path = "./course-02242-examples/src/dependencies/java/dtu/deps/simple/"

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
        classes_from_arguments = re.findall("(?:public|private)\s+(?:\S*\s+|s*)(?:\S+\s+\S+)\(\s*(\S+)(?:\[\]|<.*>)\s+\S+\s*(?:,(\S+)(?:\[\]|<.*>)\s+\S+)*\)",no_comment)
        return_types = re.findall("(?:public|private)\s+(?:\S+\s+|s*)(?:(\S+)\s+\S+)\((?:.*)\)",no_comment)    

        print("filename:", file,
              "\t| class name: ", package + class_name, 
              "\t| direct imports: ", direct_imports,
              "\t| objects created: ", new_objects )
        

        main_class = package[0] + "." if package != [] else ""
        main_class += class_name[0]

        dict[ main_class ] = direct_imports + new_objects

        # Create the graph
        # Conditions has to be improved with loop for all the list 
        dot = gv.Digraph()
        dot.node('A', file)

        if (direct_imports != []):
            dot.node('C', direct_imports[0]) 
            if dot.source.find('C') != -1:
                dot.edge('C', 'A')


        if (new_objects != []):
            dot.node('B', new_objects[0])
            dot.edge('B', 'A')
        
        if (package != []):
            dot.node('D', package[0])
            if dot.source.find('C') != -1:
                dot.edge('D', 'C')
            else:
                dot.edge('D', 'A')

    

        # print(dot.source)  
        dot.render(f'output-graph/{file}').replace('\\', '/')



def complete_dict():
    new_dict = {}
    for k, v in dict.items():
        list_complete_classes = list( filter( lambda elem: len( elem.split('.') ) > 1, v ) ) + [k]
        complete_classes = set( [ elem.split('.')[-1] for elem in list_complete_classes ] )
        short_classes = set( filter( lambda elem: len( elem.split('.') ) == 1, v ) )

        '''
        print("..")
        print(complete_classes)
        print(short_classes)
        print( "intersection:", complete_classes & short_classes )
        '''
        missing_package = short_classes - complete_classes
        # print( "in the same package (missing package):", missing_package )

        package = k.rsplit('.', 1 )[0]
        #list_complete_classes += [ package + "." + sc for sc in missing_package ]
        list_complete_classes += [ sc for sc in missing_package ]

        new_dict[k] = [elem for elem in list_complete_classes if elem != k ]

    return new_dict

print()
print( dict )



new_dict= complete_dict()

print("--")

pp.pprint(new_dict)

