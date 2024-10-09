from .errors import PyloxParseError, ErrorReporter, PyloxRuntimeError
from .expr import Binary, Unary, Literal, Grouping, Variable, Assign
from .stmt import Var, Print, Expression, Block
from .token_type import TokenType
from .tokens import Token


class Parser:
    def __init__(self, error_reporter: ErrorReporter, tokens: list[Token]):
        self.error_reporter = error_reporter
        self.tokens = tokens
        self.current = 0

    def _expression(self):
        return self._assignment()

    def _assignment(self):
        expr = self._equality()

        if self._match(TokenType.EQUAL):
            equals = self._previous()
            value = self._assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            raise PyloxRuntimeError(equals, "Invalid assignment target.")
        return expr

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
        elif self._match(TokenType.IDENTIFIER):
            return Variable(self._previous())
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

    def _declaration(self):
        try:
            if self._match(TokenType.VAR):
                return self._var_declaration()
            return self._statement()
        except PyloxParseError:
            self._synchronize()
            return None

    def _var_declaration(self):
        identifier = self._consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self._match(TokenType.EQUAL):
            initializer = self._expression()

        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Var(identifier, initializer)

    def _statement(self):
        if self._match(TokenType.PRINT):
            return self._print_statement()
        if self._match(TokenType.LEFT_BRACE):
            return self._block_statement()
        return self._expression_statement()

    def _print_statement(self):
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def _expression_statement(self):
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Expression(value)

    def _block_statement(self):
        statements = self._define_block()
        return Block(statements)

    def _define_block(self):
        statements = list()
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            statements.append(self._declaration())
        self._consume(TokenType.RIGHT_BRACE, "Expect '}' at end of block.")
        return statements

    def parse(self):
        statements = []
        while not self._is_at_end():
            statements.append(self._declaration())

        return statements
