
from types_repr import * 



def print_data_old(DATA):
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

def get_java_types():
    string = ClassRepr(class_name="String", package="java.lang", class_type="c", is_ours=False)
    string.add_method(
        MethodRepr( method_name="valueOf", parameters={"int"}, return_type="String" )
    )

    system = ClassRepr(class_name="System", package="java.lang", class_type="c", is_ours=False)
    system.add_variable( VariableRepr( var_name="out", generic="PrintStream", specific="PrintStream") )
    print_stream = ClassRepr(class_name="PrintStream", package="java.lang", class_type="c", is_ours=False)
    print_stream.add_method(
        MethodRepr( method_name="println", parameters={"String"}, return_type="void" )
    )

    array_list_string = ClassRepr(class_name="ArrayList<String>", package="java.util", class_type="c", is_ours=False)
    return [string, system, print_stream, array_list_string]

def find_class(DATA, class_name):
    found = {elem for elem in DATA if elem.class_name == class_name }
    assert len(found) <= 1
    return found.pop() if len(found) > 0 else None

def find_function(inv : InvocationRepr) -> MethodRepr:
    assert isinstance(inv.owner, ClassRepr)
    
    inv.owner.find_method( inv.method_name, inv.parameters )



def handle_static_simple(DATA, temp_type : TemporaryType) -> ClassRepr:
    elements = temp_type.variable_name.split('.')
    if len(elements) > 1:
        print("NOT SUPPORTED YET")
        return None
 
    main_class = find_class(DATA, elements.pop())
    return main_class



def complete(DATA):
    
    for class_info in DATA:
        for method in class_info.methods:
            for inv in method.invocations:
                print(inv)
                
                if type( inv.owner ) == type("") and inv.owner == "this":
                    inv.owner = class_info # it's own class class
                    continue

                inv_owner_variable = method.search_for_variable( inv.owner.variable_name )
                # print( inv.owner, inv_owner_variable )

                if inv_owner_variable is not None:
                    owner_class = find_class( DATA, inv_owner_variable.get_most_specific_type() )
                    if owner_class is not None:
                        inv.owner = owner_class
                        continue

                owner_class = handle_static_simple( DATA, inv.owner )
                if owner_class is not None:
                    inv.owner = owner_class


                print( inv.owner, inv_owner_variable )



            # second iteration
            for inv in method.invocations:
                if isinstance(inv.owner, ClassRepr):
                    # ignore for now
                    print("invocation has no defined owner yet")
                    continue


    
    
    return DATA




# Known current limitations:
# - we are not considering arguments as variables, and we should
# - we do not handle class-level variables (only local ones in the method-level)
# - we cannot yet convert functions to types
#   i.e. we don't know what type this is -> person3.getAddress(), for ex.