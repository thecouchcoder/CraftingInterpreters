from pylox.tokens import Token
from .errors import PyloxParseError, ErrorReporter
from .expr import Binary, Unary, Literal, Grouping
from .token_type import TokenType


class Parser:
    def __init__(self, error_reporter: ErrorReporter, tokens: list[Token]):
        self.error_reporter = error_reporter
        self.tokens = tokens
        self.current = 0

    def _expression(self):
        return self._equality()

    def _equality(self):
        expression = self._comparison()
        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expression = Binary(expression, operator, right)

        return expression

    def _comparison(self):
        expression = self._term()
        while self._match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self._previous()
            right = self._term()
            expression = Binary(expression, operator, right)

        return expression

    def _term(self):
        expression = self._factor()
        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self._factor()
            expression = Binary(expression, operator, right)
        return expression

    def _factor(self):
        expression = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH):
            operator = self._previous()
            right = self._unary()
            expression = Binary(expression, operator, right)
        return expression

    def _unary(self):
        if self._match(TokenType.BANG, TokenType.MINUS):
            return Unary(self._previous(), self._unary())
        return self._primary()

    def _primary(self):
        if self._match(TokenType.FALSE):
            return Literal(False)
        elif self._match(TokenType.TRUE):
            return Literal(True)
        elif self._match(TokenType.NIL):
            return Literal(None)
        elif self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)
        elif self._match(TokenType.LEFT_PAREN):
            expression = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ) after expression")
            return Grouping(expression)

        raise self._create_exception("Expect Expression")

    def _match(self, *token_types: TokenType) -> bool:
        for tt in token_types:
            if self._check(tt):
                self._advance()
                return True
        else:
            return False

    def _check(self, token_type: TokenType) -> bool:
        return self._peek().type == token_type if not self._is_at_end() else False

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise self._create_exception(message)

    def _create_exception(self, message):
        self.error_reporter.parse_error(self._peek(), message)
        raise PyloxParseError()

    def _synchronize(self):
        self._advance()
        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return

            match self._peek().type:
                case (
                    TokenType.CLASS
                    | TokenType.FUNC
                    | TokenType.VAR
                    | TokenType.FOR
                    | TokenType.IF
                    | TokenType.WHILE
                    | TokenType.PRINT
                    | TokenType.RETURN
                ):
                    return

            self._advance()

    def parse(self):
        try:
            return self._expression()
        except PyloxParseError:
            return None
