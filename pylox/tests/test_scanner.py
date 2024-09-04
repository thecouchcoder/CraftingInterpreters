import unittest

from src.errors import ErrorReporter
from src.scanner import Scanner
from src.token_type import TokenType


class ScannerTest(unittest.TestCase):
    def test_can_scan_single_tokens(self):
        source = "(){},.-+;*"
        error_reporter = ErrorReporter()
        scanner = Scanner(source, error_reporter)
        tokens = scanner.scan_tokens()
        self.assertEqual(11, len(tokens))
        self.assertFalse(error_reporter.had_error)

    def test_can_report_errors(self):
        source = "~"
        error_reporter = ErrorReporter()
        scanner = Scanner(source, error_reporter)
        tokens = scanner.scan_tokens()
        self.assertEqual(1, len(tokens))
        self.assertTrue(error_reporter.had_error)

    def test_can_scan_double_character_tokens(self):
        source = "= == ! != > >= < <"
        error_reporter = ErrorReporter()
        scanner = Scanner(source, error_reporter)
        tokens = scanner.scan_tokens()
        self.assertEqual(9, len(tokens))
        self.assertFalse(error_reporter.had_error)

    def test_can_scan_slashes_vs_comments(self):
        source = "/ // Hello world"
        error_reporter = ErrorReporter()
        scanner = Scanner(source, error_reporter)
        tokens = scanner.scan_tokens()
        self.assertEqual(2, len(tokens))
        self.assertFalse(error_reporter.had_error)

    def test_skips_whitespace(self):
        source = "var s = 123; \n\r\t s = s + 1;"
        error_reporter = ErrorReporter()
        scanner = Scanner(source, error_reporter)
        tokens = scanner.scan_tokens()
        self.assertEqual(12, len(tokens))
        self.assertFalse(error_reporter.had_error)

    def test_can_scan_book_sample(self):
        source = """// this is a comment
                (( )){} // grouping stuff
                !*+-/=<> <= == // operators"""
        error_reporter = ErrorReporter()
        scanner = Scanner(source, error_reporter)
        tokens = scanner.scan_tokens()
        self.assertEqual(17, len(tokens))
        self.assertFalse(error_reporter.had_error)

    def test_can_scan_strings(self):
        source = '"hello" "world" "goodbye world"'
        error_reporter = ErrorReporter()
        scanner = Scanner(source, error_reporter)
        tokens = scanner.scan_tokens()
        self.assertEqual(4, len(tokens))
        self.assertEqual("hello", tokens[0].literal)
        self.assertFalse(error_reporter.had_error)

    def test_can_scan_multi_line_strings(self):
        source = '''"goodbye
                  world"'''
        error_reporter = ErrorReporter()
        scanner = Scanner(source, error_reporter)
        tokens = scanner.scan_tokens()
        self.assertEqual(2, len(tokens))
        self.assertFalse(error_reporter.had_error)

    def test_can_scan_numbers(self):
        source = "123 123.456"
        error_reporter = ErrorReporter()
        scanner = Scanner(source, error_reporter)
        tokens = scanner.scan_tokens()
        self.assertEqual(3, len(tokens))
        self.assertEqual("123", tokens[0].literal)
        self.assertEqual("123.456", tokens[1].literal)
        self.assertFalse(error_reporter.had_error)

    def test_can_scan_keywords_and_identifiers(self):
        source = "if a_var and b_var"
        error_reporter = ErrorReporter()
        scanner = Scanner(source, error_reporter)
        tokens = scanner.scan_tokens()
        self.assertEqual(5, len(tokens))
        self.assertIs(tokens[0].type, TokenType.IF)
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].literal, "a_var")
        self.assertEqual(tokens[2].type, TokenType.AND)
        self.assertEqual(tokens[3].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[3].literal, "b_var")
        self.assertFalse(error_reporter.had_error)


if __name__ == "__main__":
    unittest.main()
