import unittest

from ast_printer import AstPrinter
from expr import Unary, Binary, Literal, Grouping
from lox_token import Token
from token_type import TokenType


class ASTPrinterTest(unittest.TestCase):
    def test_ast_printer(self):
        expression = Binary(
            Unary(Token(TokenType.MINUS, "-", None, 1),
                  Literal(123)),
            Token(TokenType.STAR, "*", None, 1),
            Grouping(Literal(45.67))
        )

        res = AstPrinter().print(expression)
        self.assertEqual("(* (- 123) (group 45.67))", res)
