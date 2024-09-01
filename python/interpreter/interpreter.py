from expr import Binary, Grouping, Literal, Unary
from token_type import TokenType


class Interpreter:
    def visit_binary_expr(self, expr: Binary):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)
        # Again not casting since Python is dynamic
        match expr.operator.type:
            case TokenType.MINUS:
                return left - right
            case TokenType.SLASH:
                return left / right
            case TokenType.STAR:
                return left * right
            case TokenType.PLUS:
                # No additional logic needed here since Python + already handles string concatenation and we didn't cast in the first place
                return left + right
            case TokenType.GREATER:
                return left > right
            case TokenType.GREATER_EQUAL:
                return left >= right
            case TokenType.LESS:
                return left < right
            case TokenType.LESS_EQUAL:
                return left <= right
            # Pyton equality seems to be the same as lox so no additonal logic is needed
            case TokenType.EQUAL_EQUAL:
                return left == right
            case TokenType.BANG_EQUAL:
                return not (left == right)

    def visit_grouping_expr(self, expr: Grouping):
        return self._evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_unary_expr(self, expr: Unary):
        right = self._evaluate(expr.right)
        # I did not do the casting here since Python is dynamic I believe we'll be fine
        match expr.operator.type:
            case TokenType.MINUS:
                return -right
            case TokenType.BANG:
                # Pretty sure Python's not behaves the same as Lox so no additional logic is needed
                return not right
            case _:
                return None

    def _evaluate(self, expr):
        return expr.accept(self)

    def interpret(self, expr):
        return self._evaluate(expr)
