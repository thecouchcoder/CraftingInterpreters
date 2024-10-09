import unittest
from unittest.mock import patch

from expr import Variable, Assign
from src.errors import ErrorReporter
from src.expr import Unary, Binary, Literal, Grouping
from src.interpreter import Interpreter
from src.stmt import Print, Var, Block
from src.token_type import TokenType
from src.tokens import Token


class TestInterpreter(unittest.TestCase):
    @patch("builtins.print")
    def test_interpreter(self, mock_print):
        expression = Print(
            Binary(
                Unary(
                    Token(TokenType.MINUS, "-", None, 1),
                    Literal(123.0),
                ),
                Token(TokenType.STAR, "*", None, 1),
                Grouping(Literal(45.67)),
            )
        )

        err_reporter = ErrorReporter()
        Interpreter(err_reporter).interpret([expression])

        mock_print.assert_called_with("-5617.41")

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
        Interpreter(err_reporter).interpret([expression])
        self.assertEqual(True, err_reporter.had_runtime_error)

    @patch("builtins.print")
    def test_can_concat_string(self, mock_print):
        expression = Print(
            Binary(
                Literal("hello "), Token(TokenType.PLUS, "+", None, 1), Literal("world")
            )
        )

        err_reporter = ErrorReporter()
        Interpreter(err_reporter).interpret([expression])
        mock_print.assert_called_with("hello world")

    @patch("builtins.print")
    def test_can_add_numbers(self, mock_print):
        expression = Print(
            Binary(
                Literal("1.0"),
                Token(TokenType.PLUS, "+", None, 1),
                Literal("2.0"),
            )
        )

        err_reporter = ErrorReporter()
        Interpreter(err_reporter).interpret([expression])
        mock_print.assert_called_with("3")

    # 3.0 + 2.0 == 5.0
    @patch("builtins.print")
    def test_can_compare_equality(self, mock_print):
        expression = Print(
            Binary(
                Binary(
                    Literal("3.0"), Token(TokenType.PLUS, "+", None, 1), Literal("2.0")
                ),
                Token(TokenType.EQUAL_EQUAL, "==", None, 1),
                Literal("5.0"),
            )
        )

        err_reporter = ErrorReporter()
        Interpreter(err_reporter).interpret([expression])
        mock_print.assert_called_with("True")

    # var a = 42
    # a = 100
    # print(a)
    @patch("builtins.print")
    def test_can_declare_and_use_variables(self, mock_print):
        a_token = Token(TokenType.VAR, "a", None, 1)
        declare = Var(a_token, Literal(42))
        assign = Assign(a_token, Literal(100))
        use = Print(Variable(a_token))
        program = [declare, assign, use]
        err_reporter = ErrorReporter()
        Interpreter(err_reporter).interpret(program)
        mock_print.assert_called_with("100")

    @patch("builtins.print")
    def test_can_use_lexical_scoping(self, mock_print):
        outer_token = Token(TokenType.VAR, "outer", None, 1)
        declare = Var(outer_token, Literal(42))
        use = Print(Variable(outer_token))

        inner_token = Token(TokenType.VAR, "inner", None, 1)
        inner_declare = Var(inner_token, Literal(24))
        inner_use = Print(Variable(inner_token))
        block_statements = [inner_declare, inner_use]
        block = Block(block_statements)

        program = [declare, block, use]
        err_reporter = ErrorReporter()
        Interpreter(err_reporter).interpret(program)

        mock_print.assert_any_call("42")
        mock_print.assert_any_call("24")
