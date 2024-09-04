import unittest

from src.ast_printer import AstPrinter
from src.errors import ErrorReporter
from src.parser import Parser
from src.scanner import Scanner


class TestParser(unittest.TestCase):
    def test_can_parse(self):
        test_cases = [
            ("5+3", "(+ 5 3)"),
            ("10-2*4", "(- 10 (* 2 4))"),
            ("5>3", "(> 5 3)"),
            ("5+3 != 8", "(!= (+ 5 3) 8)"),
            ("!4", "(! 4)"),
            ("-(5>3) == !false", "(== (- (group (> 5 3))) (! False))"),
        ]

        for text, expected in test_cases:
            with self.subTest(text=text, expected=expected):
                error_reporter = ErrorReporter()
                scanner = Scanner(text, error_reporter)
                tokens = scanner.scan_tokens()
                parser = Parser(error_reporter, tokens)
                expr = parser.parse()
                result = AstPrinter().print(expr)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
