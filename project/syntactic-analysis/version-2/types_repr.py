from enum import Enum
from multipledispatch import dispatch

class ClassType(Enum):
    CLASS = 1,
    INTERFACE = 2,
    BASIC = 3,

class ClassRepr():
    def __init__(self, class_name: str, class_package: str, class_type: ClassType, methods: list ):
        self.class_name = class_name
        self.class_package = class_package
        self.class_type = class_type
        self.methods = methods

    def get_name(self):
        return self.class_package + "." +  self.class_name
    
    def pprint(self):
        sstr = f"=== {self.get_name()} ===\n"
        print(sstr)
        for m in self.methods:
            m.pprint()


    def __repr__(self):
        return f"Class(type={self.class_type}, full_name={self.get_name()})"

class TempClassRepr():
    def __init__(self, specific_name: str, generic_name: str):
        self.specific_name = specific_name
        self.generic_name = generic_name

    def __repr__(self):
        return f"TempClass(specific={self.specific_name}, generic={self.generic_name})"

    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, __value: object) -> bool:
        return str(self) == str(__value)
    
    def __hash__(self) -> int:
        return hash(str(self))

class MethodRepr():
    def __init__(self, name: str, related_class: TempClassRepr, parameter_types: list, return_type: TempClassRepr, invocations: list, variables: list):
        self.name = name
        self.related_class = related_class
        self.parameter_types = parameter_types
        self.return_type = return_type
        self.invocations = invocations
        self.variables = variables

    def print_variables(self):
        return f"[MethodRepr.variables]: {', '.join( [ f'{v.name}:{v.variable_type}' for v in self.variables ] )}"

    def pprint(self):
        ret = f"+ {self.name}({', '.join([ elem.specific_name for elem in self.parameter_types ])}): {self.return_type}\n"
        for inv in self.invocations:
            ret += str(inv) + "\n"
        
        print(ret)

    def print_full(self):
        return f"{self.related_class.get_name()}.{self.name}({', '.join([ elem.specific_name for elem in self.parameter_types ])})"


    def __repr__(self):
        if isinstance(self.related_class, TempClassRepr):
            return f"[MethodRepr] {self.related_class}-{self.name}({', '.join([ elem.specific_name for elem in self.parameter_types ])}): {self.return_type}"
        return f"+ + {self.related_class.get_name()}-{self.name}({', '.join([ elem.specific_name for elem in self.parameter_types ])}): {self.return_type}"

    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, __value: object) -> bool:
        return str(self) == str(__value)
    
    def __hash__(self) -> int:
        return hash(str(self))

class TempMethodRepr():
    def __init__(self, method_name: str, related_class: TempClassRepr, parameters: list):
        self.method_name = method_name
        self.related_class = related_class
        self.parameters = parameters

    def __repr__(self):
        return f"[TempMethodRepr] {self.related_class.specific_name}-{self.method_name}({', '.join([ str(elem.specific_name) for elem in self.parameters ])})"

    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, __value: object) -> bool:
        return str(self) == str(__value)
    
    def __hash__(self) -> int:
        return hash(str(self))

class VariableRepr():
    def __init__(self, name: str, variable_type: TempClassRepr):
        self.name = name
        self.variable_type = variable_type

    def __repr__(self):
        return f"Variable(name={self.name}, type={self.variable_type})"



# TODO:
# - do the "complete" part...