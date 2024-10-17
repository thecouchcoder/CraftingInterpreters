import unittest
from unittest.mock import patch

from expr import Logical
from src.errors import ErrorReporter
from src.expr import Unary, Binary, Literal, Grouping, Variable, Assign
from src.interpreter import Interpreter
from src.stmt import Print, Var, Block, Conditional, While
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

    # var x = 0;
    # if (x == 42) print "if"
    # else print "else
    @patch("builtins.print")
    def test_can_interpret_if_else(self, mock_print):
        x_token = Token(TokenType.VAR, "x", None, 1)
        declare = Var(x_token, Literal(0))

        expression = Binary(
            Variable(Token(TokenType.IDENTIFIER, "x", "x", 1)),
            Token(TokenType.EQUAL_EQUAL, "==", None, 1),
            Literal("42"),
        )
        then_branch = Print(Literal("if"))
        else_branch = Print(Literal("else"))
        conditional = Conditional(expression, then_branch, else_branch)

        program = [declare, conditional]
        err_reporter = ErrorReporter()
        Interpreter(err_reporter).interpret(program)
        mock_print.assert_any_call("else")

    # if (x and/or y and/or z) print "truthy"
    # else print "falsy"
    @patch("builtins.print")
    def test_can_interpret_logic(self, mock_print):
        test_cases = [
            (42, 42, 42, TokenType.AND, "truthy"),
            (42, 42, None, TokenType.AND, "falsy"),
            (42, 42, 42, TokenType.OR, "truthy"),
            (42, 42, None, TokenType.OR, "truthy"),
            (None, None, None, TokenType.OR, "falsy"),
        ]
        x_token = Token(TokenType.VAR, "x", None, 1)
        y_token = Token(TokenType.VAR, "y", None, 1)
        z_token = Token(TokenType.VAR, "z", None, 1)
        and_token = Token(TokenType.AND, "and", "and", 1)
        or_token = Token(TokenType.AND, "or", "or", 1)
        then_branch = Print(Literal("truthy"))
        else_branch = Print(Literal("falsy"))

        for x, y, z, op, expected in test_cases:
            declare_x = Var(x_token, Literal(x))
            declare_y = Var(y_token, Literal(y))
            declare_z = Var(z_token, Literal(z))

            op1 = and_token if op == TokenType.AND else or_token
            op2 = and_token if op == TokenType.AND else or_token
            expression = Logical(
                Logical(Variable(x_token), op1, Variable(y_token)),
                op2,
                Variable(z_token),
            )

            conditional = Conditional(expression, then_branch, else_branch)

            program = [declare_x, declare_y, declare_z, conditional]
            err_reporter = ErrorReporter()
            Interpreter(err_reporter).interpret(program)
            mock_print.assert_any_call(expected)

    # while (x < 4) { print x; x = x+1; }
    @patch("builtins.print")
    def test_can_interpret_while_loop(self, mock_print):
        x_token = Token(TokenType.VAR, "x", "x", 1)
        declare_x = Var(x_token, Literal(0))

        x_variable = Variable(Token(TokenType.IDENTIFIER, "x", "x", 1))
        while_stmt = While(
            Binary(
                x_variable,
                Token(TokenType.LESS, "<", None, 1),
                Literal("4"),
            ),
            Block(
                [
                    Print(x_variable),
                    Assign(
                        x_token,
                        Binary(
                            x_variable, Token(TokenType.PLUS, "+", None, 1), Literal(1)
                        ),
                    ),
                ]
            ),
        )

        program = [declare_x, while_stmt]
        err_reporter = ErrorReporter()
        Interpreter(err_reporter).interpret(program)
        mock_print.assert_any_call("0")
        mock_print.assert_any_call("1")
        mock_print.assert_any_call("2")
        mock_print.assert_any_call("3")
        # mock_print.assert_called_with("4")
