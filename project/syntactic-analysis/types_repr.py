
def helper_print_arguments( parameter_set: set ):
    if parameter_set == set():
        return "()"

    temp_parameter_set = [ str(elem) for elem in parameter_set ]
    return f"( { '.'.join( temp_parameter_set )} )"
    

class TemporaryType:
    def __init__(self, var_name = None, method_name = None):
        self.variable_name = var_name
        self.method_name = method_name

    def __str__(self):
        return f"TEMP_TYPE({self.variable_name if self.variable_name is not None else '-'}, {self.method_name if self.method_name is not None else '-'})"

    def __repr__(self) -> str:
        return f"TemporaryType({self.variable_name}, {self.method_name})"
    
    def __eq__(self, __value: object) -> bool:
        return repr(self) == repr(__value)
    
    def __hash__(self):
        return hash(repr(self))
    
    def __format__(self,fmt):
        return f'{str(self):{fmt}}' 


class VariableRepr():
    def __init__(self, var_name, generic = None, specific = None):
        self.name = var_name
        self.generic = generic
        self.specific = specific

    def get_most_specific_type(self):
        return self.specific if self.specific is not None else self.generic

    def __str__(self):
        return f"VariableRepr({self.name}, {self.generic}, {self.specific})"

    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, __value: object) -> bool:
        return repr(self) == repr(__value)
    
    def __hash__(self):
        return hash(repr(self))
    
    def __format__(self,fmt):
        return f'{str(self):{fmt}}' 



class InvocationRepr():
    def __init__(self, method_name, parameters, owner):
        self.method_name = method_name
        self.parameters : list[str | TemporaryType ] = parameters
        self.owner : list[str | TemporaryType | ClassRepr ] = owner
    
    def pretty_name(self):
        return f"{self.method_name}{helper_print_arguments(self.parameters)}"
    
    def __str__(self):
        return f"InvocationRepr({self.method_name}, {self.parameters}, {self.owner})"

    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, __value: object) -> bool:
        return repr(self) == repr(__value)
    
    def __hash__(self):
        return hash(repr(self))
    
    def __format__(self,fmt):
        return f'{str(self):{fmt}}' 

class MethodRepr():
    def __init__(self, method_name, parameters, return_type):
        self.method_name : str = method_name
        self.parameters : list[str] = parameters
        self.return_type : str = return_type

        self.invocations : set[InvocationRepr] = set()
        self.variables : set[VariableRepr] = set()

    def add_invocation( self, inv : InvocationRepr ):
        # TODO: verify if there is one just equal
        self.invocations.add( inv )

    def add_variable( self, var : VariableRepr):
        # TODO: verify if there is one just equal
        self.variables.add( var )

    def search_for_variable(self, var_name: str):
        res = { var for var in self.variables if var.name == var_name }
        return res.pop() if len(res) > 0 else None

    def pretty_name(self):
        return f"{self.method_name}{helper_print_arguments(self.parameters)} : {self.return_type}"

    def __str__(self):
        return f"{self.method_name}{helper_print_arguments(self.parameters)} : {self.return_type}"

    def __repr__(self) -> str:
        return f"{self.method_name}{helper_print_arguments(self.parameters)} : {self.return_type}"
    
    def __eq__(self, __value: object) -> bool:
        return repr(self) == repr(__value)
    
    def __hash__(self):
        return hash(repr(self))
    
    def __format__(self,fmt):                
        return f'{str(self):{fmt}}' 


class ClassRepr():
    def __init__(self, class_name, package, class_type, is_ours=True):
        self.class_name = class_name
        self.package = package
        self.is_ours = is_ours
        self.class_type = class_type

        self.methods = list[MethodRepr] = []
        self.variables : list[VariableRepr] = set()

    def add_method(self, method: MethodRepr ):
        self.methods.append( method )

    def add_variable(self, var: VariableRepr ):
        self.variables.add( var )

    def find_variable(self, var_name: str) -> VariableRepr:
        found = { var for var in self.variables if var.name == var_name }
        return found.pop() if len(found) > 0 else None
    
    def find_method(self, method_name, parameters) -> MethodRepr:
        pass

    def pretty_name(self):
        return f"({self.class_type}) {self.package}.{self.class_name}"

    def __str__(self):
        return f"({self.class_type}) {self.package}.{self.class_name}"

    def __repr__(self) -> str:
        return f"({self.class_type}) {self.package}.{self.class_name}"
    
    def __eq__(self, __value: object) -> bool:
        return str(self) == str(__value)
    
    def __hash__(self):
        return hash(str(self))

    def __format__(self,fmt):                
        return f'{str(self):{fmt}}' 
    
