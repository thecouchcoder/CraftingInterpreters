from pylox.token_type import TokenType
from pylox.tokens import Token


class PyloxRuntimeError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message

    def __str__(self):
        return f"{self.message} \n[line {self.token.line}]"


class PyloxParseError(Exception):
    pass


class ErrorReporter:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

    def error(self, line: int, message: str):
        self._report(line, "", message)

    def parse_error(self, token: Token, message: str):
        if token.type == TokenType.EOF:
            self._report(token.line, " at end", message)
        self._report(token.line, f" at '{token.lexeme}'", message)

    def runtime_error(self, err: PyloxRuntimeError):
        print(err)
        self.had_runtime_error = True

    def _report(self, line: int, where: str, message: str):
        print("[line " + str(line) + "] Error " + where + ": " + message)
        self.had_error = True
