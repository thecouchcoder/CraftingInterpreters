from error_reporter import ErrorReporter
from lox_token import Token
from token_type import TokenType, get_keyword


class Scanner:
    def __init__(self, source: str, error_reporter: ErrorReporter):
        self.source = source
        self.error_reporter: ErrorReporter = error_reporter
        self.tokens: list[Token] = []
        self.line: int = 1
        self.start: int = 0
        self.current: int = 0
        return

    def scan_tokens(self) -> list[Token]:
        while not self.at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self):
        c = self.advance()
        match c:
            case '(':
                self.add_token(TokenType.LEFT_PAREN)
            case ')':
                self.add_token(TokenType.RIGHT_PAREN)
            case '{':
                self.add_token(TokenType.LEFT_BRACE)
            case '}':
                self.add_token(TokenType.RIGHT_BRACE)
            case ',':
                self.add_token(TokenType.COMMA)
            case '.':
                self.add_token(TokenType.DOT)
            case '-':
                self.add_token(TokenType.MINUS)
            case '+':
                self.add_token(TokenType.PLUS)
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '*':
                self.add_token(TokenType.STAR)
            case '=':
                self.add_token(TokenType.EQUAL_EQUAL) if self.match('=') else self.add_token(TokenType.EQUAL)
            case '!':
                self.add_token(TokenType.BANG_EQUAL) if self.match('=') else self.add_token(TokenType.BANG)
            case '>':
                self.add_token(TokenType.GREATER_EQUAL) if self.match('=') else self.add_token(TokenType.GREATER)
            case '<':
                self.add_token(TokenType.LESS_EQUAL) if self.match('=') else self.add_token(TokenType.LESS)
            case '/':
                if self.match('/'):
                    self.add_comment()
                else:
                    self.add_token(TokenType.SLASH)
            case ' ' | '\r' | '\t':
                pass
            case '"':
                self.add_string()
            case c if self.is_digit(c):
                self.add_number()
            case c if self.is_alpha(c):
                self.add_identifier()
            case '\n':
                self.line += 1
            case _:
                self.error_reporter.error(self.line, "Unexpected character")

    def is_digit(self, c: str) -> bool:
        return '0' <= c <= '9'

    def is_alpha(self, c: str) -> bool:
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'

    def add_token(self, token_type: TokenType, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def add_comment(self):
        while (peek := self.peek()) not in ('/0', "\n"):
            self.advance()

    def add_string(self):
        while (peek := self.peek()) not in ('/0', '"'):
            self.advance()
            if peek == '\n':
                self.line += 1

        if self.peek() == "/0":
            self.error_reporter.error(self.line, "Unterminated string")
            return

        self.advance()
        self.add_token(TokenType.STRING, self.source[self.start + 1:self.current - 1])

    def add_number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(TokenType.NUMBER, self.source[self.start:self.current])

    def add_identifier(self):
        while (peek := self.peek()) and self.is_alpha(peek) or self.is_digit(peek):
            self.advance()

        identifier = self.source[self.start:self.current]
        if keyword := get_keyword(identifier):
            self.add_token(keyword, identifier)
        else:
            self.add_token(TokenType.IDENTIFIER, identifier)

    # check if the next character matches, if so consume it and return True else return False
    def match(self, next_c: str) -> bool:
        peek = self.peek()
        if peek == '/0' or peek != next_c:
            return False

        self.advance()
        return True

    # consume a character
    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    # check next character, but don't consume
    def peek(self) -> str:
        return self.source[self.current] if not self.at_end() else '/0'

    # 2 character lookahead
    def peek_next(self) -> str:
        return self.source[self.current + 1] if not self.current + 1 >= len(self.source) else '/0'
