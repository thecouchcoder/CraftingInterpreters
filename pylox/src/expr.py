

class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.value == other.value 
        )

class Binary:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

    def __eq__(self, other):
        return (
            self.left == other.left and
            self.operator == other.operator and
            self.right == other.right 
        )

class Grouping:
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

    def __eq__(self, other):
        return (
            self.expression == other.expression 
        )

class Literal:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

    def __eq__(self, other):
        return (
            self.value == other.value 
        )

class Unary:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

    def __eq__(self, other):
        return (
            self.operator == other.operator and
            self.right == other.right 
        )

class Variable:
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)

    def __eq__(self, other):
        return (
            self.name == other.name 
        )