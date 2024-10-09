from expr import Assign
from .environment import Environment
from .errors import PyloxRuntimeError, ErrorReporter
from .expr import Binary, Grouping, Literal, Unary, Variable
from .stmt import Expression, Print, Var, Block
from .token_type import TokenType
from .tokens import Token


class Interpreter:
    def __init__(self, err_reporter: ErrorReporter):
        self.err_reporter = err_reporter
        self.env = Environment()

    def visit_binary_expr(self, expr: Binary):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)
        match expr.operator.type:
            case TokenType.MINUS:
                self._validate_number(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.SLASH:
                self._validate_number(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self._validate_number(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.PLUS:
                return self._validate_plus(expr.operator, left, right)
            case TokenType.GREATER:
                self._validate_number(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self._validate_number(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self._validate_number(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self._validate_number(expr.operator, left, right)
                return float(left) <= float(right)
            # Pyton equality seems to be the same as src so no additonal logic is needed
            case TokenType.EQUAL_EQUAL:
                return str(left) == str(right)
            case TokenType.BANG_EQUAL:
                return not (str(left) == str(right))

    def visit_grouping_expr(self, expr: Grouping):
        return self._evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_unary_expr(self, expr: Unary):
        right = self._evaluate(expr.right)
        match expr.operator.type:
            case TokenType.MINUS:
                self._validate_number(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                # Pretty sure Python's not behaves the same as Lox so no additional logic is needed
                return not right
            case _:
                return None

    def visit_variable_expr(self, expr: Variable):
        return self.env.get(expr.name)

    def visit_assign_expr(self, expr: Assign):
        value = self._evaluate(expr.value)
        self.env.assign(expr.name, value)
        return value

    def visit_expression_stmt(self, stmt: Expression):
        self._evaluate(stmt.expression)

    def visit_print_stmt(self, stmt: Print):
        value = self._evaluate(stmt.expression)
        print(self._stringify_expression_result(value))

    def visit_var_stmt(self, stmt: Var):
        value = None
        if stmt.initializer:
            value = self._evaluate(stmt.initializer)
        self.env.define(stmt.name.lexeme, value)

    def visit_block_stmt(self, stmt: Block):
        block_env = Environment(self.env)
        self._execute_block(stmt.statements, block_env)

    def _evaluate(self, expr):
        return expr.accept(self)

    def _validate_number(self, operator: Token, *operands):
        for o in operands:
            try:
                float(o)
            except:
                raise PyloxRuntimeError(operator, f"{o} must be a number")

    def _validate_plus(self, operator: Token, left, right):
        try:
            lf = float(left)
            rf = float(right)
            return lf + rf
        except:
            # TODO not really sure if this is right, but the book doesn't give any examples
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            elif isinstance(left, str):
                raise PyloxRuntimeError(
                    operator, f"{left} and {right} must both be strings"
                )
            else:
                raise PyloxRuntimeError(
                    operator, f"{left} and {right} must both a numbers"
                )

    def _stringify_expression_result(self, value):
        if value is None:
            return "nil"

        text = str(value)
        if isinstance(value, float):
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return text

    def _execute(self, stmt):
        stmt.accept(self)

    def _execute_block(self, statements: list, env: Environment):
        previous = self.env
        try:
            self.env = env
            for statement in statements:
                self._execute(statement)
        finally:
            self.env = previous

    def interpret(self, statements: list):
        try:
            for stmt in statements:
                self._execute(stmt)
        except PyloxRuntimeError as err:
            self.err_reporter.runtime_error(err)
