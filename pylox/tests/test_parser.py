import unittest

from src.ast_printer import AstPrinter
from src.errors import ErrorReporter
from src.expr import Literal, Binary, Assign
from src.parser import Parser
from src.scanner import Scanner
from src.stmt import Print, Var, Expression
from src.token_type import TokenType
from src.tokens import Token


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


if __name__ == "__main__":
    unittest.main()
