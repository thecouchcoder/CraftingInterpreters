from .errors import PyloxRuntimeError
from .tokens import Token


class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self._values = dict()

    def define(self, identifier: str, value):
        self._values[identifier] = value

    def get(self, name: Token):
        if name.lexeme in self._values:
            return self._values[name.lexeme]
        elif self.enclosing is not None:
            return self.enclosing.get(name)
        else:
            raise PyloxRuntimeError(name, f"Undefined variable {name.lexeme}.")

    def assign(self, name: Token, value):
        self.get(name)
        self.define(name.lexeme, value)
