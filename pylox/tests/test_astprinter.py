import unittest

from src.ast_printer import AstPrinter
from src.expr import *
from src.token_type import TokenType
from src.tokens import Token


class ASTPrinterTest(unittest.TestCase):
    def test_ast_printer(self):
        expression = Binary(
            Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
            Token(TokenType.STAR, "*", None, 1),
            Grouping(Literal(45.67)),
        )

        res = AstPrinter().print(expression)
        self.assertEqual("(* (- 123) (group 45.67))", res)
