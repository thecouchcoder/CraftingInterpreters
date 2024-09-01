import { TokenType } from "./tokenType";

export class Token {
  constructor(
    readonly tokenType: TokenType,
    readonly lexeme: string,
    readonly literal: string | number,
    readonly line: number
  ) {}

  toString(): string {
    return `${TokenType[this.tokenType]} ${this.lexeme} ${this.literal}`;
  }
}
