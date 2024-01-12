from collections import defaultdict
from types_repr import *

class SyntaxFold:
    def visit(self, node):
        results = [self.visit(n) for n in node.children]

        if hasattr(self, node.type):
            return getattr(self, node.type)(node, results)

        return self.default(node, results)

    def default(self, node, results):
        return set().union(*results)
    
class ClassInfo(SyntaxFold):
    def __init__(self):
        self.class_package = None
        self.class_name = None
        self.class_type = None
        self.methods = []

    def program(self, node, results):
        for child in node.children:
            self.visit(child)
        
        # for m in self.methods:
        #     m.related_class = TempClassRepr(self.class_name, self.class_name)
        return set()

    def package_declaration(self, node, results):
        for child in node.children:
            self.visit(child) 
        return set()
    
    def scoped_identifier(self, node, results):
        # > sets SELF.CLASS_PACKAGE
        # used only for package, called above!

        if node.parent.type != "package_declaration":
            return set()
        
        self.class_package = node.text.decode()
        return set()
    
    def class_declaration(self, node, results):
        self.class_name = node.child_by_field_name("name").text.decode()
        self.class_type = ClassType.CLASS
        #for child in node.children:
        #    self.visit(child)
        return set()
    
    def interface_declaration(self, node, results):
        self.class_name = node.child_by_field_name("name").text.decode()
        self.class_type = ClassType.INTERFACE
        #for child in node.children:
        #    self.visit(child)
        return set()

    # TODO: maybe delete
    def class_body(self, node, results):
        return set()
    
    def constructor_declaration(self, node, results):

        # - at this point, we don't have self.class_name filled...
        # temp_self_class = TempClassRepr(self.class_name, self.class_name)

        # - find out:
        # parameter_types = []
        # invocations = []
        # variables = []

        method_info = MethodInfo()
        method_info.visit(node)
                                            # we don't know this at this point :c
        constr = MethodRepr( name=method_info.name, related_class=None, parameter_types=method_info.parameter_types, return_type=method_info.return_type, invocations=method_info.invocations, variables=method_info.variables)
        self.methods.append( constr )
        
        return set()
    
    def method_declaration(self, node, results):
        method_info = MethodInfo()
        method_info.visit(node)
        constr = MethodRepr( name=method_info.name, related_class=None, parameter_types=method_info.parameter_types, return_type=method_info.return_type, invocations=method_info.invocations, variables=method_info.variables)

        self.methods.append( constr )
        return set()



    def __repr__(self):
        return f"ClassInfo(package={self.class_package}, name={self.class_name}, type={self.class_type})"
    

class MethodInfo(SyntaxFold):
    def __init__(self):
        self.name = None

        # we don't know this info at this point...
        # TODO: maybe remove it
        self.related_class = None

        self.parameter_types = []
        self.return_type = None
        self.invocations = []
        self.variables = []

    def constructor_declaration(self, node, results):
        self.return_type = self.related_class
        self.name = "<init>"
        self.return_type = "<this>"
        self.visit( node.child_by_field_name("parameters") )
        return set()
    
    def method_declaration(self, node, results):
        self.name = node.child_by_field_name("name").text.decode()
        self.return_type = node.child_by_field_name("type").text.decode()
        self.visit( node.child_by_field_name("parameters") )
        return set()
    
    def local_variable_declaration(self, node, results):
        var_name = node.child_by_field_name("declarator").child_by_field_name("name").text.decode()
        var_type = node.child_by_field_name("type").text.decode()
        var_rep = VariableRepr(name=var_name, variable_type=TempClassRepr(var_type, var_type))

        self.variables.append( var_rep)
        return set()

    def formal_parameters(self, node, results):
        parameter_types_str = [ child.child_by_field_name("type").text.decode() for child in node.children if child.child_by_field_name("type") is not None]
        parameter_names_str = [ child.child_by_field_name("name").text.decode() for child in node.children if child.child_by_field_name("name") is not None]

        assert (len(parameter_types_str) == len(parameter_names_str))

        self.parameter_types = [ TempClassRepr(elem, elem) for elem in parameter_types_str ]
        self.variables = [ VariableRepr(name=parameter_names_str[i], variable_type=param_type) for i, param_type in enumerate(parameter_types_str) ]
        return set()
    
    def  object_creation_expression(self, node, results):
        class_type = node.child_by_field_name("type").text.decode()
        func_name = "<init>"

        args = [ self.visit(elem).pop() for elem in node.children_by_field_name("arguments") if len(self.visit(elem)) > 0]
        args_class = [ TempClassRepr(elem, elem) for elem in args ]

        inv = TempMethodRepr(method_name=func_name, related_class=TempClassRepr(class_type, class_type), parameters=args_class)
        self.invocations.append( inv )

        return set()
    
    def method_invocation(self, node, results):
        obj = node.child_by_field_name("object")
        variable_name = obj.text.decode() if obj is not None else "<this>"
        func_name = node.child_by_field_name("name").text.decode()

        related_class_str = None

        # this means it is a class!!!
        # for ex. a static function
        if variable_name not in [ elem.name for elem in self.variables ]:
            # in this case, this "variable name" will be a class (or <this>)
            related_class_str = variable_name
        else:
            related_class_str = [ elem.variable_type.specific_name for elem in self.variables if elem.name == variable_name ][0]

        args = []
        for elem in node.child_by_field_name("arguments").children:
            visit_res = self.visit(elem)
            if len(visit_res) > 0:
                args.append( self.visit(elem).pop() )

        args_class = [ TempClassRepr(elem, elem) for elem in args ]
        inv = TempMethodRepr(method_name=func_name, related_class=TempClassRepr(related_class_str,related_class_str), parameters=args_class)
        self.invocations.append( inv )

        return set()
    
    # only used to find out invocation arguments
    def identifier(self, node, results):
        if node.parent.type != "argument_list":
            return set()
        
        var_name = node.text.decode()
        assert var_name in [ elem.name for elem in self.variables ]

        return { [ elem.variable_type.specific_name for elem in self.variables if elem.name == var_name ][0] }
        
    # only used to find out invocation arguments
    def string_literal(self, node, results):
        if node.parent.type != "argument_list":
            return set()
        return {"String"}
    
    # only used to find out invocation arguments
    def  decimal_integer_literal(self, node, results):
         return { "int" }

    def __repr__(self):
        return f"MethodInfo(name={self.name}, related_class={self.related_class}, params={self.parameter_types}, variables={self.variables})"
    
    