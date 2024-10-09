import unittest

from src.environment import Environment
from src.errors import PyloxRuntimeError
from src.token_type import TokenType
from src.tokens import Token


class EnvironmentTests(unittest.TestCase):
    def test_can_get_and_set_variables(self):
        env = Environment()
        token = Token(TokenType.VAR, "my_var", "", 1)

        env.define("my_var", 42)
        self.assertEqual(env.get(token), 42)

        env.define("my_var", 365)
        self.assertEqual(env.get(token), 365)

    def test_unknown_variable_throws_runtime_exception(self):
        env = Environment()
        token = Token(TokenType.VAR, "unknown_var", "", 1)
        self.assertRaises(PyloxRuntimeError, env.get, token)

    def test_can_assign(self):
        env = Environment()
        token = Token(TokenType.VAR, "my_var", "", 1)
        env.define("my_var", 42)
        env.assign(token, 100)

        self.assertEqual(env.get(token), 100)

    def test_assigning_unknown_variable_throws_runtime_exception(self):
        env = Environment()
        token = Token(TokenType.VAR, "my_var", "", 1)

        self.assertRaises(PyloxRuntimeError, env.assign, token, 100)

    def test_can_use_scope(self):
        global_env = Environment()
        global_env.define("global_var", "42")

        block_env = Environment(global_env)
        block_env.define("block_var", "inner_42")

        self.assertEqual(block_env.get(Token(TokenType.VAR, "global_var", "", 1)), "42")
        self.assertEqual(
            block_env.get(Token(TokenType.VAR, "block_var", "", 1)), "inner_42"
        )

        # redefine global var within block scope
        block_env.define("global_var", "not 42")

        self.assertEqual(
            block_env.get(Token(TokenType.VAR, "global_var", "", 1)), "not 42"
        )
        # Should be the same in the global env
        self.assertEqual(
            global_env.get(Token(TokenType.VAR, "global_var", "", 1)), "42"
        )
