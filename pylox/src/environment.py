from .errors import PyloxRuntimeError
from .tokens import Token


class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values = dict()

    def define(self, identifier: str, value):
        self.values[identifier] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        elif self.enclosing is not None:
            return self.enclosing.get(name)
        else:
            raise PyloxRuntimeError(name, f"Undefined variable {name.lexeme}.")

    def assign(self, name: Token, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        elif self.enclosing is not None:
            self.enclosing.assign(name, value)
        else:
            raise PyloxRuntimeError(name, f"Undefined variable {name.lexeme}.")
