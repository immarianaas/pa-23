
def helper_print_arguments( parameter_set: set ):
    if parameter_set == set():
        return "()"

    temp_parameter_set = [ str(elem) for elem in parameter_set ]
    return f"( { '.'.join( temp_parameter_set )} )"
    

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



def complete(DATA):
    
    for class_info in DATA:
        for method in class_info.methods:
            for inv in method.invocations:
                
                if type( inv.owner ) == type(""):
                    print("string ---> " + inv.owner)
                    continue

                inv_owner = method.search_for_variable( inv.owner.variable_name )
                print( inv.owner, inv_owner )
            # I want to convert TEMP_TYPE into String or ClassRepr
    
    

    new_data = {}




# Known current limitations:
# - we are not considering arguments as variables, and we should
# - we do not handle class-level variables (only local ones in the method-level)
# - we cannot yet convert functions to types
#   i.e. we don't know what type this is -> person3.getAddress(), for ex.