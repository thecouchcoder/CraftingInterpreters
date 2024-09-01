import unittest

from pylox.expr import Unary, Binary, Literal, Grouping
from pylox.interpreter import Interpreter
from pylox.token_type import TokenType
from pylox.tokens import Token


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
