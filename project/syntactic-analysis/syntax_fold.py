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
    def class_declaration(self, node, results):
        print( dir(node) )
        if node.parent.type != "program":
            return set()

        names = node.children_by_field_name("name")
        return {name.text for name in names}

    def class_body(self, node, results):
        return set()


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


class FunctionFunctions(SyntaxFold):
    def __init__( self, function_name):
        self.funct_name = function_name

    def method_declaration(self, node, results):
        # if node.parent.type != "program":
        #     return set()

        print(node.children)

        print()


        func = node.child_by_field_name("name")
        annotations = self.visit( node.child )
        print( func.parent )
        print("annotations", annotations)
        print("function", func.text)

        
        print()


        return {}        
        #functions = node.children_by_field_name("name")


        #functions = node.children_by_field_name("name")
        
        #func = [ func for func in functions if func.text == self.funct_name ]
        #assert len(func) == 1

        #return self.visit(func)
    
    def modifiers(self, node, results):
        return { self.visit( child ) for child in node.children }
    
    def identifiers(self, node, results):
        return { node.text }

    def marker_annotation(self, node, results):
        annotations = node.children_by_field_name("name")
        assert len(annotations) == 1

        return { annotations[0].text }



class AnnotationName(SyntaxFold):
    def modifiers(self, node, results):
        return [ self.visit( child ) for child in node.children ]
    
    def identifiers(self, node, results):
        return node.text


