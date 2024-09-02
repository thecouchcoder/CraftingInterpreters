import unittest

from pylox.errors import ErrorReporter
from pylox.expr import Unary, Binary, Literal, Grouping
from pylox.interpreter import Interpreter
from pylox.token_type import TokenType
from pylox.tokens import Token


class TestInterpreter(unittest.TestCase):
    def test_interpreter(self):
        expression = Binary(
            Unary(
                Token(TokenType.MINUS, "-", None, 1),
                Literal(123.0),
            ),
            Token(TokenType.STAR, "*", None, 1),
            Grouping(Literal(45.67)),
        )

        err_reporter = ErrorReporter()
        result = Interpreter(err_reporter).interpret(expression)

        self.assertEqual(-5617.41, result)

    # 2 * (3 / -"muffin")
    def test_invalid_expression(self):
        expression = Binary(
            Literal(2),
            Token(TokenType.STAR, "*", None, 1),
            Grouping(
                Binary(
                    Literal(3),
                    Token(TokenType.SLASH, "/", None, 1),
                    Unary(Token(TokenType.MINUS, "-", None, 1), Literal("muffin")),
                )
            ),
        )

        err_reporter = ErrorReporter()
        result = Interpreter(err_reporter).interpret(expression)
        self.assertEqual(True, err_reporter.had_runtime_error)

    def test_can_concat_string(self):
        expression = Binary(
            Literal("hello "), Token(TokenType.PLUS, "+", None, 1), Literal("world")
        )

        err_reporter = ErrorReporter()
        result = Interpreter(err_reporter).interpret(expression)
        self.assertEqual("hello world", result)

    def test_can_add_numbers(self):
        expression = Binary(
            Literal("1.0"), Token(TokenType.PLUS, "+", None, 1), Literal("2.0")
        )

        err_reporter = ErrorReporter()
        result = Interpreter(err_reporter).interpret(expression)
        self.assertEqual(3.0, result)
