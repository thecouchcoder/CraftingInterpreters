class Block:
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)

    def __eq__(self, other):
        return self.statements == other.statements


class Expression:
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

    def __eq__(self, other):
        return self.expression == other.expression


class Conditional:
    def __init__(self, condition, if_stmt, else_stmt):
        self.condition = condition
        self.if_stmt = if_stmt
        self.else_stmt = else_stmt

    def accept(self, visitor):
        return visitor.visit_conditional_stmt(self)

    def __eq__(self, other):
        return (
            self.condition == other.condition
            and self.if_stmt == other.if_stmt
            and self.else_stmt == other.else_stmt
        )


class Print:
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

    def __eq__(self, other):
        return self.expression == other.expression


class Var:
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_stmt(self)

    def __eq__(self, other):
        return self.name == other.name and self.initializer == other.initializer


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)

    def __eq__(self, other):
        return self.condition == other.condition and self.body == other.body
