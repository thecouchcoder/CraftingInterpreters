

class Block:
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)

    def __eq__(self, other):
        return (
            self.statements == other.statements 
        )

class Expression:
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

    def __eq__(self, other):
        return (
            self.expression == other.expression 
        )

class Print:
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

    def __eq__(self, other):
        return (
            self.expression == other.expression 
        )

class Var:
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_stmt(self)

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.initializer == other.initializer 
        )