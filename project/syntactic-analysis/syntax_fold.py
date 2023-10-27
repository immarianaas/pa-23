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
        if node.parent.type != "program":
            return set()

        names = node.children_by_field_name("name")
        return {name.text for name in names}

    def class_body(self, node, results):
        return set()
