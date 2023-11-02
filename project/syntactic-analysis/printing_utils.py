
from types_repr import * 


def print_data(DATA):
    for class_info in DATA:
        print("-"*50)
        print(f"|{'':10s}{class_info.pretty_name():36s}  |")
        print("-"*50)

        for method in class_info.methods:
            func_str = f"| - {method.pretty_name()}"
            print( '|   '+'-'*(len(func_str)-4) )
            print( func_str )

            for inv in method.invocations:
                print(f"| - - {inv.owner:30s}...{inv.pretty_name()}")
            
            for inv in method.final_invocations:
                print(f"| - * {inv.pretty_name()}")



def get_java_types():
    string = ClassRepr(class_name="String", package="java.lang", class_type="c", is_ours=False)
    string.add_method(
        MethodRepr( method_name="valueOf", parameters={"int"}, return_type="String" )
    )
    string.add_method(
        MethodRepr( method_name="concat", parameters={"String"}, return_type="String" )
    )

    system = ClassRepr(class_name="System", package="java.lang", class_type="c", is_ours=False)
    system.add_variable( VariableRepr( var_name="out", generic="PrintStream", specific="PrintStream") )
    print_stream = ClassRepr(class_name="PrintStream", package="java.lang", class_type="c", is_ours=False)
    print_stream.add_method(
        MethodRepr( method_name="println", parameters={"String"}, return_type="void" )
    )
    print_stream.add_method(
        MethodRepr( method_name="println", parameters={}, return_type="void" )
    )

    array_list_string = ClassRepr(class_name="ArrayList<String>", package="java.util", class_type="c", is_ours=False)



    return [string, system, print_stream, array_list_string ] + get_basic_java_types()

def get_basic_java_types():
    ret = []
    ret.append( ClassRepr(class_name="int", package="-", class_type="b", is_ours=False) )
    ret.append( ClassRepr(class_name="float", package="-", class_type="b", is_ours=False) )
    ret.append( ClassRepr(class_name="void", package="-", class_type="b", is_ours=False) )
    ret.append( ClassRepr(class_name="bool", package="-", class_type="b", is_ours=False) )
    ret.append( ClassRepr(class_name="double", package="-", class_type="b", is_ours=False) )
    return ret



def find_class(DATA, class_name):
    found = {elem for elem in DATA if elem.class_name == class_name }
    assert len(found) <= 1
    return found.pop() if len(found) > 0 else None

def find_function(inv : InvocationRepr) -> MethodRepr:
    assert isinstance(inv.owner, ClassRepr)
    
    inv.owner.find_method( inv.method_name, inv.parameters )

def handle_static(DATA, temp_type: TemporaryType) -> ClassRepr:
    elements = temp_type.variable_name.split('.')

    if not elements[0][0].isupper():
        print(elements)
        return None
        

    main_class : ClassRepr = find_class(DATA, elements[0])
    for elem in elements[1:]:

        if main_class is None:
            break

        var_class = None

        if elem[-1] == ')':
            main_class.find_method( elem, [] ) # TODO: this won't work bc of arguments

        else:
            var = main_class.find_variable( elem )
            var_class = find_class(DATA, var.get_most_specific_type())


        main_class = var_class
    
    return main_class


def handle_invocation_owner(DATA, inv: InvocationRepr):
    print(inv)

def search_method_return_return(DATA, inv:InvocationRepr):
    inv_method = inv.owner.find_method( inv.method_name, inv.parameters )
    if inv_method is not None:
        return inv_method.return_type

def set_function_owner(DATA, inv: InvocationRepr, curr_class: ClassRepr, method: MethodRepr ):
    if isinstance(inv.owner, str) and inv.owner == "this":
        inv.owner = curr_class # it's own class class
        ret = search_method_return_return(DATA, inv)
        return ret
    
    if isinstance(inv.owner, TemporaryType):
        inv_owner_variable = method.search_for_variable( inv.owner.variable_name )

        if inv_owner_variable is not None:
            owner_class = find_class( DATA, inv_owner_variable.get_most_specific_type() )
            if owner_class is not None:
                inv.owner = owner_class
                print(inv.owner)
                ret = search_method_return_return(DATA, inv)
                return ret
        
        # if it is not variable, it might be static
        owner_class = handle_static( DATA, inv.owner )
        inv.owner = "~None~" if owner_class is None else owner_class # might be None
        return inv.owner
    
    if isinstance(inv.owner, InvocationRepr):
        inv_owner_variable = None # TODO here
        print("TO BE PROCESSED", inv.owner)

        owner_class = set_function_owner( DATA, inv.owner, curr_class, method )
        
        inv.owner = owner_class

        print(inv)
        ret = search_method_return_return(DATA, inv)
        return ret if ret is not None else inv.owner


    return owner_class

def get_class_from_repr(DATA, repr: VariableRepr | TemporaryType | str, method: MethodRepr ):

    class_name = None
    variable = None

    if isinstance(repr, VariableRepr):
        class_name = repr.get_most_specific_type()
    elif isinstance(repr, TemporaryType):
        variable = method.search_for_variable(repr.variable_name)
        class_name = variable.get_most_specific_type() if variable is not None else variable
    elif isinstance( repr, str):
        class_name = repr

    if class_name is None:
        print("ERROR CLASS_NAME is None:", repr)

    arg_class = find_class(DATA, class_name)
    if  arg_class is None and variable is not None:
        if not isinstance(variable, InvocationRepr):
            arg_class = handle_static( DATA, variable )
        else:
            arg_class = set_function_owner(DATA, variable)

    if arg_class is None:
        print("!!get_class_from_repr returning None", repr)
    return arg_class


def complete(DATA):
    for class_info in DATA:
        for method in class_info.methods:

            return_class = get_class_from_repr( DATA, method.return_type, method)
            method.return_type = return_class

            method.parameters = [ get_class_from_repr(DATA, param, method) for param in method.parameters]


    for class_info in DATA:
        for method in class_info.methods:

            #return_class = get_class_from_repr( DATA, method.return_type, method)
            #method.return_type = return_class

            #method.parameters = [ get_class_from_repr(DATA, param, method) for param in method.parameters]

            if return_class is None:
                print( "NO RETURN CLASS -", method.return_type)
            for inv in method.invocations:

                new_params : list[ ClassRepr ] = []
                for arg in inv.parameters:
                    """
                    class_name = arg
                    variable = None

                    if isinstance(arg, VariableRepr):
                        class_name = arg.get_most_specific_type()
                    elif isinstance(arg, TemporaryType):
                        variable = method.search_for_variable(arg.variable_name)
                        class_name = variable.get_most_specific_type() if variable is not None else variable
                    
                    arg_class = find_class(DATA, class_name)
                    if  arg_class is None and variable is not None:
                        if not isinstance(variable, InvocationRepr):
                            arg_class = handle_static( DATA, variable )
                        else:
                            arg_class = handle_invocation_owner(DATA, variable)

                    new_params.append( arg_class )
                    """
                    new_params.append( get_class_from_repr(DATA, arg, method) )
                inv.parameters = new_params

                set_function_owner(DATA, inv, class_info, method )

                """
                if isinstance(inv.owner, str) and inv.owner == "this":
                    inv.owner = class_info # it's own class class
                    continue

                if isinstance(inv.owner, InvocationRepr):
                    inv_owner_variable = None # TODO here
                else:
                    inv_owner_variable = method.search_for_variable( inv.owner.variable_name )

                if inv_owner_variable is not None:
                    owner_class = find_class( DATA, inv_owner_variable.get_most_specific_type() )
                    if owner_class is not None:
                        inv.owner = owner_class
                        continue

                if not isinstance( inv.owner, InvocationRepr ):
                    owner_class = handle_static( DATA, inv.owner )
                else:
                    owner_class = handle_invocation_owner(DATA, inv.owner)

                if owner_class is not None:
                    inv.owner = owner_class
                """


    # second iteration
    for class_info in DATA:
        for method in class_info.methods:
            for inv in method.invocations:
                if not isinstance(inv.owner, ClassRepr):
                    # ignore for now
                    print("invocation has no defined owner yet", inv)
                    continue

                found_method = inv.owner.find_method( inv.method_name, inv.parameters )
                if found_method is not None:
                    method.add_final_invocation( found_method )
                else:
                    print("::: method not found:", inv.owner, inv.method_name, inv.parameters)



    
    
    return DATA




# Known current limitations:
# - we are not considering arguments as variables, and we should
# - we do not handle class-level variables (only local ones in the method-level)
# - we cannot yet convert functions to types
#   i.e. we don't know what type this is -> person3.getAddress(), for ex.