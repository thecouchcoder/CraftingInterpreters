import unittest

from expr import Unary, Binary, Literal, Grouping
from interpreter import Interpreter
from lox_token import Token
from token_type import TokenType


class TestInterpreter(unittest.TestCase):
    def test_interpreter(self):
        expression = Binary(
            Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
            Token(TokenType.STAR, "*", None, 1),
            Grouping(Literal(45.67)),
        )

        interpreter = Interpreter()
        result = interpreter._evaluate(expression)

        self.assertEqual(-5617.41, result)
