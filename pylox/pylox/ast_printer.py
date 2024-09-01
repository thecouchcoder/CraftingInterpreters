from pylox.expr import Unary, Literal, Grouping, Binary


class AstPrinter:

    def __init__(self):
        self.name = "AstPrinter"

    def print(self, expr):
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs):
        s = f"({name}"
        for expr in exprs:
            s += f" {expr.accept(self)}"
        s += ")"
        return s

    def visit_binary_expr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal):
        if expr.value is None:
            return None
        return expr.value

    def visit_unary_expr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)
