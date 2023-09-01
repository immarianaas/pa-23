import os
import re
import pprint 
import graphviz as gv
import glob

pp = pprint.PrettyPrinter(indent=4)

lookup_table = {
    "String": "java.lang.String",
    "Integer": "java.lang.Integer"
}

#maybe change the wrong name
primitive_types = { "int", "byte", "short", "long", "float", "double", "boolean", "char", "void" }

#path = "./course-02242-examples/src/dependencies/java/dtu/deps/tricky/"
path = "./course-02242-examples/src/dependencies/java/dtu/deps/simple/"
proj_path = "./course-02242-examples/src"
# { principal class : [ immediate dependencies ] }
dict = {}

def create_graph():
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

def strip_elems( l ):
    return [ elem.strip() for elem in l]


# for file in os.listdir( path ):
# for file in glob.iglob("**/*.java", recursive=True):
for file in glob.iglob(proj_path+"/**/*.java", recursive=True):
    print( file )
    with open(file) as f:

        src_code = f.read()

        no_comment = re.sub( "/\*(?:[^*]|\*(?!/s))*\*/", "", src_code)
        no_comment = re.sub( "//.*\n", "", no_comment)

        # print(src_code)
        # print("no commentt" + no_comment)
         

        package = strip_elems( re.findall(r"(?<=package\s)[\s\S]+?(?=;)", no_comment ) )
        class_name = strip_elems( re.findall(r"(?<=class\s)[\s\S]+?(?=\{|implements|extends)", no_comment ))


        direct_imports = strip_elems( re.findall(r"(?<=import\s)[\s\S]+?(?=;)", no_comment ) )
        new_objects = strip_elems( re.findall(r"(?<=new\s)[\s\S]+?(?=\(|<)", no_comment ) )


        # TODO: change pattern to match only what is before < ---> "Iterator<Integer>" should be 2: Interator and Integer
        #       (in this case doesn't really matter )
        classes_from_arguments = re.findall(r"(?:public|private)\s+(?:\S*\s+|s*)(?:\S+\s+\S+)\(\s*(\S+)(?:\[\]|<.*>)\s+\S+\s*(?:,(\S+)(?:\[\]|<.*>)\s+\S+)*\)",no_comment)
        classes_from_arguments = [ elem for tup in classes_from_arguments for elem in tup if elem != '' and elem not in primitive_types ]
        return_types = [ elem for elem in re.findall(r"(?:public|private)\s+(?:\S+\s+|s*)(?:(\S+)\s+\S+)\((?:.*)\)",no_comment) if elem != "void" and elem not in primitive_types ]

        '''
        print("filename:", file,
              "\t| class name: ", package + class_name, 
              "\t| direct imports: ", direct_imports,
              "\t| objects created: ", new_objects )
        '''

        main_class = package[0] + "." if package != [] else ""
        main_class += class_name[0]


        dict[ main_class ] = direct_imports + new_objects + classes_from_arguments + return_types

        # Create the graph
        create_graph()


def is_complete_class( c ):
    return len( c.split('.') ) > 1

def is_asterisk_class( c ):
    return len( c.split('.') ) > 1 and c[-1] == '*'

def is_short_class( c ):
    return len( c.split('.') ) == 1


def find_package( short_class, package, asterisk_classes, total_complete_classes ):
    global lookup_table

    if package + "." + short_class in total_complete_classes:
        return package + "." + short_class
    
    for ac in asterisk_classes:
        possible_class = ac[:-1] + short_class
        print( "possible_class", possible_class )
        if possible_class in total_complete_classes:
            return possible_class
        
    if short_class in lookup_table:
        return lookup_table[short_class]
        
    return "WILL BE IGNORED: " + short_class


def complete_dict():
    # complete single classes
    all_classes = list( dict.keys() ) + [ elem for l in dict.values() for elem in l ]
    total_complete_classes = [ elem for elem in all_classes if is_complete_class( elem ) and not is_asterisk_class(elem) ]

    new_dict = {}
    for k, v in dict.items():
        list_complete_classes = list( filter( is_complete_class, v ) ) + [k]
        complete_classes_short = set( [ elem.split('.')[-1] for elem in list_complete_classes ] )
        short_classes = set( filter( is_short_class, v ) )

        '''
        print("..")
        print(complete_classes)
        print(short_classes)
        print( "intersection:", complete_classes & short_classes )
        '''
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



new_dict= complete_dict()

pp.pprint(new_dict)

