import { reportError } from "./errorReporter";
import { Token } from "./token";
import { TokenType, KeywordToTokenType } from "./tokenType";

export class Scanner {
  private start: number = 0;
  private current: number = 0;
  private line: number = 1;
  private tokens: Token[] = [];

  constructor(private readonly source: string) {}
  scanTokens(): Token[] {
    while (!this.isAtEnd()) {
      this.start = this.current;
      this.scanToken();
    }

    this.tokens.push(new Token(TokenType.EOF, "", null, this.line));
    return this.tokens;
  }

  private isAtEnd(): Boolean {
    return this.current >= this.source.length;
  }

  private scanToken() {
    let c = this.advance();
    switch (c) {
      // Single character
      case "(": {
        this.extractToken(TokenType.LEFT_PAREN);
        break;
      }
      case ")": {
        this.extractToken(TokenType.RIGHT_PAREN);
        break;
      }
      case "{": {
        this.extractToken(TokenType.LEFT_BRACE);
        break;
      }
      case "}": {
        this.extractToken(TokenType.RIGHT_BRACE);
        break;
      }
      case ",": {
        this.extractToken(TokenType.COMMA);
        break;
      }
      case ".": {
        this.extractToken(TokenType.DOT);
        break;
      }
      case "-": {
        this.extractToken(TokenType.MINUS);
        break;
      }
      case "+": {
        this.extractToken(TokenType.PLUS);
        break;
      }
      case ";": {
        this.extractToken(TokenType.SEMICOLON);
        break;
      }
      case "*": {
        this.extractToken(TokenType.STAR);
        break;
      }

      // double characters
      case "!": {
        this.extractToken(
          this.match("=") ? TokenType.BANG_EQUAL : TokenType.BANG
        );
        break;
      }
      case "=": {
        this.extractToken(
          this.match("=") ? TokenType.EQUAL_EQUAL : TokenType.EQUAL
        );
        break;
      }
      case "<": {
        this.extractToken(
          this.match("=") ? TokenType.LESS_EQUAL : TokenType.LESS
        );
        break;
      }
      case ">": {
        this.extractToken(
          this.match("=") ? TokenType.GREATER_EQUAL : TokenType.GREATER
        );
        break;
      }
      case "/": {
        if (this.match("/")) {
          this.extractComment();
        } else {
          this.extractToken(TokenType.SLASH);
        }
        break;
      }
      case " ":
      case "\r":
      case "\t":
        break;

      case "\n":
        this.line++;
        break;
      case '"':
        this.extractString();
        break;
      default: {
        if (this.isDigit(c)) {
          this.extractNumber();
        } else if (this.isAlpha(c)){
          this.extractIdentifier()
        }
        else {
          reportError(this.line, "Unexpected character.");
        }
      }
    }
  }

  private advance(): string {
    return this.source[this.current++];
  }

  private peek(n: number = 0): string {
    if (this.isAtEnd()) return "\0";
    return this.source[this.current + n];
  }

  private extractToken(type: TokenType, literal: string | number = null) {
    let token = new Token(
      type,
      this.source.substring(this.start, this.current),
      literal,
      this.line
    );
    this.tokens.push(token);
  }

  private match(next: string): Boolean {
    if (this.isAtEnd()) {
      return false;
    }
    if (this.source[this.current] != next) {
      return false;
    }

    this.current++;
    return true;
  }

  private extractComment() {
    let next = this.peek();
    while (next != "\n" && next != "\0") {
      this.advance();
      next = this.peek();
    }
  }

  private extractString() {
    let next = this.peek();
    while (next != '"' && next != "\0") {
      if (next == "\n") {
        this.line++;
      }
      this.advance();
      next = this.peek();
    }

    if (next == "\0") {
      reportError(this.line, "Unterminated string");
      return;
    }

    this.advance();

    let s = this.source.substring(this.start + 1, this.current - 1);
    this.extractToken(TokenType.STRING, s);
  }

  private isDigit(c: string): Boolean {
    return c >= "0" && c <= "9";
  }

  private isAlpha(c: string): boolean {
    return (c >= "a" && c <= "z") || (c >= "A" && c <= "Z") || c == "_";
  }

  private extractNumber() {
    let next = this.peek();
    while (this.isDigit(next) || (next == "." && this.isDigit(this.peek(1)))) {
      this.advance();
      next = this.peek();
    }

    if (next == "." && !this.isDigit(this.peek(1))) {
      // consume the offending period
      this.advance();
      reportError(this.line, "Not a valid number");
      return;
    }

    let n = this.source.substring(this.start, this.current);
    this.extractToken(TokenType.NUMBER, parseFloat(n));
  }

  private extractIdentifier() {
    let next = this.peek();
    while(this.isAlpha(next) || this.isDigit(next)) {
      this.advance();
      next = this.peek();
    }

    const identifier = this.source.substring(this.start, this.current);
    let type = TokenType.IDENTIFIER
    if (KeywordToTokenType.hasOwnProperty(identifier)) {
      type = KeywordToTokenType[identifier];
    }
    this.extractToken(type);
  }
}
