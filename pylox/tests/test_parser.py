import unittest

from src.ast_printer import AstPrinter
from src.errors import ErrorReporter
from src.expr import Literal, Binary, Assign, Variable, Logical, Grouping
from src.parser import Parser
from src.scanner import Scanner
from src.stmt import Print, Var, Expression, Conditional
from src.token_type import TokenType
from src.tokens import Token
from stmt import While, Block


class TestParser(unittest.TestCase):
    def test_can_parse_simple_expression(self):
        test_cases = [
            ("5+3;", "(+ 5 3)"),
            ("10-2*4;", "(- 10 (* 2 4))"),
            ("5>3;", "(> 5 3)"),
            ("5+3 != 8;", "(!= (+ 5 3) 8)"),
            ("!4;", "(! 4)"),
            ("-(5>3) == !false;", "(== (- (group (> 5 3))) (! False))"),
        ]

        for text, expected in test_cases:
            with self.subTest(text=text, expected=expected):
                error_reporter = ErrorReporter()
                scanner = Scanner(text, error_reporter)
                tokens = scanner.scan_tokens()
                parser = Parser(error_reporter, tokens)
                stmts = parser.parse()
                result = AstPrinter().print(stmts[0].expression)
                self.assertEqual(result, expected)

    def test_can_parse_program(self):
        program = 'print "one"; print true; print 2 + 1; var a = 42; a=100;'
        error_reporter = ErrorReporter()
        scanner = Scanner(program, error_reporter)
        tokens = scanner.scan_tokens()
        parser = Parser(error_reporter, tokens)
        ast = parser.parse()

        expected_stmt_0 = Print(Literal("one"))
        self.assertEqual(expected_stmt_0, ast[0])

        expected_stmt_1 = Print(Literal(True))
        self.assertEqual(expected_stmt_1, ast[1])

        expected_stmt_2 = Print(
            Binary(Literal("2"), Token(TokenType.PLUS, "+", None, 1), Literal("1"))
        )
        self.assertEqual(expected_stmt_2, ast[2])

        a_id = Token(TokenType.IDENTIFIER, "a", "a", 1)
        expected_stmt_3 = Var(a_id, Literal("42"))
        self.assertEqual(expected_stmt_3, ast[3])

        expected_stmt_4 = Expression(Assign(a_id, Literal("100")))
        self.assertEqual(expected_stmt_4, ast[4])

    def test_can_parse_if_statement(self):
        program = 'if (x == 42) print "if";'
        error_reporter = ErrorReporter()
        scanner = Scanner(program, error_reporter)
        tokens = scanner.scan_tokens()
        parser = Parser(error_reporter, tokens)
        ast = parser.parse()

        expression = Binary(
            Variable(Token(TokenType.IDENTIFIER, "x", "x", 1)),
            Token(TokenType.EQUAL_EQUAL, "==", None, 1),
            Literal("42"),
        )
        branch = Print(Literal("if"))
        expected_stmt_0 = Conditional(expression, branch, None)
        self.assertEqual(expected_stmt_0, ast[0])

    def test_can_parse_if_else_statement(self):
        program = 'if (x == 42) print "if"; else print "else";'
        error_reporter = ErrorReporter()
        scanner = Scanner(program, error_reporter)
        tokens = scanner.scan_tokens()
        parser = Parser(error_reporter, tokens)
        ast = parser.parse()

        expression = Binary(
            Variable(Token(TokenType.IDENTIFIER, "x", "x", 1)),
            Token(TokenType.EQUAL_EQUAL, "==", None, 1),
            Literal("42"),
        )
        then_branch = Print(Literal("if"))
        else_branch = Print(Literal("else"))
        expected_stmt_0 = Conditional(expression, then_branch, else_branch)
        self.assertEqual(expected_stmt_0, ast[0])

    def test_can_parse_nested_if_statement(self):
        program = 'if (x == 42) if (y == 42) print "if"; else print "else";'
        error_reporter = ErrorReporter()
        scanner = Scanner(program, error_reporter)
        tokens = scanner.scan_tokens()
        parser = Parser(error_reporter, tokens)
        ast = parser.parse()

        if_expression = Binary(
            Variable(Token(TokenType.IDENTIFIER, "x", "x", 1)),
            Token(TokenType.EQUAL_EQUAL, "==", None, 1),
            Literal("42"),
        )
        inner_if_expression = Binary(
            Variable(Token(TokenType.IDENTIFIER, "y", "y", 1)),
            Token(TokenType.EQUAL_EQUAL, "==", None, 1),
            Literal("42"),
        )
        then_branch = Print(Literal("if"))
        else_branch = Print(Literal("else"))
        expected_stmt_0 = Conditional(
            if_expression,
            Conditional(inner_if_expression, then_branch, else_branch),
            None,
        )

        self.assertEqual(expected_stmt_0, ast[0])

    def test_can_parse_logical_operators(self):
        test_cases = [
            (
                "x and y and z;",
                Expression(
                    Logical(
                        Logical(
                            Variable(Token(TokenType.IDENTIFIER, "x", "x", 1)),
                            Token(TokenType.AND, "and", "and", 1),
                            Variable(Token(TokenType.IDENTIFIER, "y", "y", 1)),
                        ),
                        Token(TokenType.AND, "and", "and", 1),
                        Variable(Token(TokenType.IDENTIFIER, "z", "z", 1)),
                    )
                ),
            ),
            (
                "x or y or z;",
                Expression(
                    Logical(
                        Logical(
                            Variable(Token(TokenType.IDENTIFIER, "x", "x", 1)),
                            Token(TokenType.OR, "or", "or", 1),
                            Variable(Token(TokenType.IDENTIFIER, "y", "y", 1)),
                        ),
                        Token(TokenType.OR, "or", "or", 1),
                        Variable(Token(TokenType.IDENTIFIER, "z", "z", 1)),
                    )
                ),
            ),
            (
                "x and y or z;",
                Expression(
                    Logical(
                        Logical(
                            Variable(Token(TokenType.IDENTIFIER, "x", "x", 1)),
                            Token(TokenType.AND, "and", "and", 1),
                            Variable(Token(TokenType.IDENTIFIER, "y", "y", 1)),
                        ),
                        Token(TokenType.OR, "or", "or", 1),
                        Variable(Token(TokenType.IDENTIFIER, "z", "z", 1)),
                    )
                ),
            ),
            (
                "x and (y or z);",
                Expression(
                    Logical(
                        Variable(Token(TokenType.IDENTIFIER, "x", "x", 1)),
                        Token(TokenType.AND, "and", "and", 1),
                        Grouping(
                            Logical(
                                Variable(Token(TokenType.IDENTIFIER, "y", "y", 1)),
                                Token(TokenType.OR, "or", "or", 1),
                                Variable(Token(TokenType.IDENTIFIER, "z", "z", 1)),
                            )
                        ),
                    )
                ),
            ),
        ]
        error_reporter = ErrorReporter()

        for program, expected in test_cases:
            scanner = Scanner(program, error_reporter)
            tokens = scanner.scan_tokens()
            parser = Parser(error_reporter, tokens)
            ast = parser.parse()
            self.assertEqual(expected, ast[0])

    def test_can_parse_while_loop(self):
        program = "while (x < 4) { print x; }"
        x = Variable(Token(TokenType.IDENTIFIER, "x", "x", 1))
        expected = While(
            Binary(
                x,
                Token(TokenType.LESS, "<", None, 1),
                Literal("4"),
            ),
            Block([Print(x)]),
        )

        error_reporter = ErrorReporter()
        scanner = Scanner(program, error_reporter)
        tokens = scanner.scan_tokens()
        parser = Parser(error_reporter, tokens)
        ast = parser.parse()
        self.assertEqual(expected, ast[0])

    def test_can_parse_for_loop(self):
        print_stmt = Print(Literal("42"))
        x_token = Token(TokenType.IDENTIFIER, "x", "x", 1)
        x_variable = Variable(x_token)
        assign_x = Assign(
            x_token,
            Binary(x_variable, Token(TokenType.PLUS, "+", None, 1), Literal("1")),
        )

        test_cases = [
            (
                "for (;;){ print 42; }",
                While(Literal(True), Block([print_stmt])),
            ),
            (
                "for (;; x=x+1){ print 42; }",
                While(
                    Literal(True), Block([Block([print_stmt]), Expression(assign_x)])
                ),
            ),
            (
                "for (; x < 4; x=x+1){ print 42; }",
                While(
                    Binary(
                        x_variable,
                        Token(TokenType.LESS, "<", None, 1),
                        Literal("4"),
                    ),
                    Block([Block([print_stmt]), Expression(assign_x)]),
                ),
            ),
            (
                "for (var x = 0; x < 4; x=x+1){ print 42; }",
                Block(
                    [
                        Var(x_token, Literal("0")),
                        While(
                            Binary(
                                x_variable,
                                Token(TokenType.LESS, "<", None, 1),
                                Literal("4"),
                            ),
                            Block([Block([print_stmt]), Expression(assign_x)]),
                        ),
                    ]
                ),
            ),
        ]

        error_reporter = ErrorReporter()
        for program, expected in test_cases:
            scanner = Scanner(program, error_reporter)
            tokens = scanner.scan_tokens()
            parser = Parser(error_reporter, tokens)
            ast = parser.parse()
            self.assertEqual(expected, ast[0])


if __name__ == "__main__":
    unittest.main()
