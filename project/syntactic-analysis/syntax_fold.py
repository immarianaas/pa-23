from collections import defaultdict
from printing_utils import *
from types_repr import *

class SyntaxFold:
    def visit(self, node):
        results = [self.visit(n) for n in node.children]

        if hasattr(self, node.type):
            return getattr(self, node.type)(node, results)

        return self.default(node, results)

    def default(self, node, results):
        return set().union(*results)

class PackageName(SyntaxFold):
    def package_declaration(self, node, results):
        ret = [c.text for c in node.children if c.type == "scoped_identifier"]
        return set(ret)
    
# get the main class name of the file
class ClassName(SyntaxFold):
    def __init__(self, package_name):
        self.data = defaultdict(list)
        self.class_repr = None
        self.package_name = package_name

    def class_declaration(self, node, results):
        # print( dir(node) )
        if node.parent.type != "program":
            return set()

        self.class_repr = ClassRepr( node.child_by_field_name("name").text.decode(), self.package_name, "c" )
        # self.data["class"] += [name.text for name in names]
        return set() # {name.text for name in names}

    def interface_declaration(self, node, results):
        self.class_repr = ClassRepr( node.child_by_field_name("name").text.decode(), self.package_name, "i" )
        return set()
    
    def enum_declaration(self, node, results):
        self.class_repr = ClassRepr( node.child_by_field_name("name").text.decode(), self.package_name, "e" )
        return set()

    def class_body(self, node, results):
        return set()

'''
class FunctionCode(SyntaxFold):
    def __init__( self, function_name):
        self.funct_name = function_name

    def method_declaration(self, node, results):
        # if node.parent.type != "program":
        #     return set()

        functions = node.children_by_field_name("name")
        
        func = [ func for func in functions if func.text == self.funct_name ]
        assert len(func) == 1

        return self.visit(func)
'''


class FunctionFunctions(SyntaxFold):
    def __init__( self, class_repr):
        self.class_repr = class_repr


        self.data = defaultdict(list)
        

    def method_declaration(self, node, results):
        # if node.parent.type != "program":
        #     return set()

        # print("children", node.children)
        function_name = node.child_by_field_name("name")
        #print("function name=", function_name.text)

        annotations = { self.visit(elem).pop() for elem in node.children if elem.type == "modifiers" and self.visit(elem) != set()}
        #print("annotations= ", annotations)

        parameters = { self.visit(elem).pop() for elem in node.children_by_field_name("parameters") if self.visit(elem) != set()}
        #print("parameters=", parameters)

        return_type = self.visit(node.child_by_field_name("type")).pop()

        this_method_repr = MethodRepr( 
                method_name=function_name.text.decode(), 
                parameters=parameters, # list of VariableRepr
                return_type= return_type, # list of strings
                variables=parameters
                # function calls missing!
            )
        
        
        function_block = FunctionBlock( this_method_repr )
        function_block.visit(node) 
        
        self.class_repr.add_method(
            this_method_repr
        )


        # self.data[function_name.text.decode()] += [ 
        #     MethodRepr(  )
        #     ,
        #     {
        #         "annotations": annotations,
        #         "parameters": parameters,
        #         "function_calls": function_block.data,
        #         "return": return_type
        #     }
        # ]


        return set()

    def marker_annotation(self, node, results):
        annotations = node.children_by_field_name("name")
        assert len(annotations) == 1
        return { annotations[0].text.decode() }
    
    def formal_parameter(self, node, results):
        param_type = node.children_by_field_name("type")
        param_name = node.children_by_field_name("name")
        assert len(param_type) == 1 and len(param_name) == 1

        #return { param_type[0].text.decode() }
        return { VariableRepr(var_name=param_name[0].text.decode(), specific=param_type[0].text.decode()) }
    
    def type_identifier(self, node, results):
        if node.parent.type != "method_declaration":
            return set()
        
        return { node.text.decode() }
    
    def integral_type(self, node, results):
        if node.parent.type != "method_declaration":
            return set()
        
        return { "int" }
    
    def floating_point_type(self, node, results):
        if node.parent.type != "method_declaration":
            return set()
        
        return { "float" }
    
    def boolean_type(self, node, results):
        if node.parent.type != "method_declaration":
            return set()
        
        return { "bool" }
    
    def void_type(self, node, results):
        if node.parent.type != "method_declaration":
            return set()
        
        return { "void" }
    
    def generic_type(self, node, results):
        if node.parent.type != "method_declaration":
            return set()
        return { node.text.decode() }




class FunctionBlock(SyntaxFold):
    def __init__(self, outter_function):
        self.data = defaultdict(list)
        self.variables = {}

        self.outter_function : MethodRepr = outter_function

    # def block( self, node, results):
    #     print("um here")
    #     return set()
    
    def method_invocation(self, node, results):
        if node.parent.type == "argument_list":
            func_name = node.child_by_field_name("name").text.decode()
            # a detail here: since we are not including args, 
            # we don't fully handle overload

            variable = node.child_by_field_name("object")
            if variable is not None:
                variable = node.text.decode()            

            return  { TemporaryType(var_name=variable, method_name=func_name ) }
            

            # return  { "unknown(methodinv)" }
        
        if node.parent.type == "variable_declarator":
            # int a = bbb.fun()
            # this will be "bbb"
            print("-->>> unknown(methodinv)", node.text.decode())
            return  { "unknown(methodinv)" }
            #return  { TemporaryType(var_name=node.text.decode()) }


        owner = "this"

        # object that is calling this object
        variable = node.child_by_field_name("object")
        if variable is not None:
            owner = variable.text.decode()

            if owner != "this" and variable.type == "method_invocation":
                owner = self.visit(variable).pop()
            elif owner != "this":
                owner = TemporaryType( var_name=owner )
            
        

        names = { self.visit(elem).pop() for elem in node.children_by_field_name("name") if self.visit(elem) != set()}
        assert len(names) == 1
        name = names.pop()

        args = { self.visit(elem).pop() for elem in node.children_by_field_name("arguments") if self.visit(elem) != set()}
        repeated_args = [ params["parameters"] == args for params in self.data[ name ] ]

        if any(repeated_args):
            return names
        
        inv = InvocationRepr( name, args, owner )
        self.outter_function.add_invocation(inv)

        """
        self.data[ name ] += [
            {
                "parameters" : args,
                "invoking": owner
            }
        ]
        """

        return { inv }
    
    def local_variable_declaration(self, node, results):
        generic_type = node.child_by_field_name("type").text.decode()
        var_name = node.child_by_field_name("declarator").child_by_field_name("name").text.decode()

        if node.child_by_field_name("declarator").child_by_field_name("value") is not None:
            specifics =self.visit(node.child_by_field_name("declarator").child_by_field_name("value")).pop()
        else:
            specifics = set()
        print(generic_type, var_name, specifics)

        self.outter_function.add_variable(
            VariableRepr( var_name= var_name, generic=generic_type, specific=None if len(specifics) == 0 else specifics )
        )

        """
        self.variables[var_name] = {
            "generic" : generic_type,
            "specific": None if len(specifics) == 0 else specifics
            
        }
        """

        return set()
    
    def object_creation_expression(self, node, results):
        return { node.child_by_field_name("type").text.decode() }
    
    def string_literal(self, node, results):
        if node.parent.type not in [ "argument_list", "variable_declarator"]:
            return set()
        
        return { "String" }
    
    def decimal_integer_literal(self, node, results):
        if node.parent.type not in [ "argument_list", "variable_declarator"]:
            return set()
        
        return { "int" }
    
    def decimal_integer_literal(self, node, results):
        if node.parent.type not in [ "argument_list", "variable_declarator"]:
            return set()
        
        return { "int" }
    
    def decimal_floating_point_literal(self, node, results):
        if node.parent.type not in [ "argument_list", "variable_declarator"]:
            return set()
        
        return { "float" }    

    def binary_expression(self, node, results):
        if node.parent.type not in [ "argument_list", "variable_declarator"]:
            return set()
                
        return self.visit( node.child_by_field_name("left") )


    def identifier(self, node, results):
        if node.parent.type not in [ "argument_list", "variable_declarator", "field_access"]:
            return { node.text.decode() }
        
        # return { "unknown, var: " + node.text.decode() }
        return { TemporaryType(var_name=node.text.decode()) }
