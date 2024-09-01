import {Token} from "./token";
import {Binary, Expr, Grouping, Literal, Unary} from "./expr";
import {TokenType} from "./tokenType";
import {error} from "./errorReporter";

export class Parser {
    private readonly tokens: Token[];
    private current: number;

    constructor(tokens: Token[]) {
        this.tokens = tokens;
        this.current = 0;
    }

    parse() {
        try {
            return this.expression();
        } catch (err) {
            return null;
        }
    }

    private expression(): Expr {
        return this.equality();
    }

    // a == b == c == d == e
    private equality(): Expr {
        // if (this.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)) {
        //     console.error("Equality with no left operand");
        //     this.synchronize();
        // }
        let expr = this.comparison();

        while (this.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)) {
            const operator = this.previous();
            let right = this.comparison();
            expr = new Binary(expr, operator, right);
        }

        return expr;
    }

    // a > b
    private comparison(): Expr {
        let expr = this.term();

        while (this.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL)) {
            const operator = this.previous();
            let right = this.term();
            expr = new Binary(expr, operator, right);
        }

        return expr;
    }

    private term(): Expr {
        let expr = this.factor();

        while (this.match(TokenType.MINUS, TokenType.PLUS)) {
            const operator = this.previous();
            let right = this.factor();
            expr = new Binary(expr, operator, right);
        }

        return expr;
    }

    private factor(): Expr {
        let expr = this.unary();

        while (this.match(TokenType.SLASH, TokenType.STAR)) {
            const operator = this.previous();
            let right = this.unary();
            expr = new Binary(expr, operator, right);
        }

        return expr;
    }

    private unary(): Expr {
        if (this.match(TokenType.BANG, TokenType.MINUS)) {
            return new Unary(this.previous(), this.unary());
        }

        return this.primary();
    }

    private primary(): Expr {
        if (this.match(TokenType.TRUE)) return new Literal(true);
        if (this.match(TokenType.FALSE)) return new Literal(false);
        if (this.match(TokenType.NIL)) return new Literal(null);
        if (this.match(TokenType.NUMBER, TokenType.STRING)) return new Literal(this.previous().literal);

        if (this.match(TokenType.LEFT_PAREN)) {
            const expression = this.expression();
            this.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.");
            return new Grouping(expression);
        }

        throw new ParseError(this.peek(), "Expect expression");
    }

    private match(...types: TokenType[]): boolean {
        for (const type of types) {
            if (this.check(type)) {
                this.advance();
                return true;
            }
        }
        return false;
    }

    private check(type: TokenType) {
        if (this.isAtEnd()) {
            return false;
        }

        return this.peek().tokenType == type;
    }

    private advance(): Token {
        if (!this.isAtEnd()) {
            this.current++;
        }
        return this.previous();
    }

    private isAtEnd() {
        return this.peek().tokenType == TokenType.EOF;
    }

    private peek() {
        return this.tokens[this.current];
    }

    private previous(): Token {
        return this.tokens[this.current - 1];
    }

    private consume(type: TokenType, message: string) {
        if (this.check(type)) {
            return this.advance();
        }

        throw new ParseError(this.peek(), message);
    }

    private synchronize() {
        this.advance();

        while (!this.isAtEnd()) {
            if (this.previous().tokenType == TokenType.SEMICOLON) return;

            switch (this.peek().tokenType) {
                case TokenType.CLASS:
                case TokenType.FUNC:
                case TokenType.VAR:
                case TokenType.FOR:
                case TokenType.IF:
                case TokenType.WHILE:
                case TokenType.PRINT:
                case TokenType.RETURN:
                    return;
            }

            this.advance();
        }
    }
}

class ParseError extends Error {
    constructor(token: Token, message: string) {
        super();
        error(token, message);
    }
}