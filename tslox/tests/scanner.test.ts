import { hadError } from "../interpreter/errorReporter";
import { Scanner } from "../interpreter/scanner";
import { Token } from "../interpreter/token";
import { TokenType } from "../interpreter/tokenType";

test("can scan basic source into Tokens", () => {
  let source = 'var language = "lox";';
  let scanner = new Scanner(source);
  let tokens = scanner.scanTokens();

  expect(tokens.length).toBe(6);
  const hasStringLiteral = tokens.some((token) => token.literal === "lox");
  expect(hasStringLiteral).toBe(true);

  const hasKeyword = tokens.some((token) => token.tokenType == TokenType.VAR);
  expect(hasKeyword).toBe(true);

  const hasIdentifier  = tokens.some((token) => token.tokenType == TokenType.IDENTIFIER);
  expect(hasIdentifier).toBe(true)
});

test("can all characters into tokens", () => {
  let source = "(){},.-+;* = != == < <= > >= /";
  let scanner = new Scanner(source);
  let tokens = scanner.scanTokens();

  expect(tokens.length).toBe(19);
});

test("can properly handle comments", () => {
  let source = `
  // this is a comment
  (( )){} // grouping stuff
  !*+-/=<> <= == // operators
  `;
  let scanner = new Scanner(source);
  let tokens = scanner.scanTokens();

  expect(tokens.length).toBe(17);
});

test("can parse numbers", () => {
  let source = "var x = 123 + 123.45";
  let scanner = new Scanner(source);
  let tokens = scanner.scanTokens();

  expect(tokens.length).toBe(7);

  const hasIntLiteral = tokens.some((token) => token.literal === 123);
  expect(hasIntLiteral).toBe(true);

  const hasDecimalLiteral = tokens.some((token) => token.literal === 123.45);
  expect(hasDecimalLiteral).toBe(true);
});

test("properly handles numbers ending in decimal point", () => {
  let source = "var x = 123. + 123.somethingelse";
  let scanner = new Scanner(source);
  let tokens = scanner.scanTokens();

  expect(hadError).toBe(true);
});

test("has error when scanning invalid source", () => {
  let source = '@#^var language = "badlox";';
  let scanner = new Scanner(source);
  let tokens = scanner.scanTokens();

  expect(hadError).toBe(true);
});

test.each([
    ["and", TokenType.AND],
    ["class", TokenType.CLASS],
    ["else", TokenType.ELSE],
    ["false", TokenType.FALSE],
    ["func", TokenType.FUNC],
    ["for", TokenType.FOR],
    ["if", TokenType.IF],
    ["nil", TokenType.NIL],
    ["or", TokenType.OR],
    ["print", TokenType.PRINT],
    ["return", TokenType.RETURN],
    ["super", TokenType.SUPER],
    ["this", TokenType.THIS],
    ["true", TokenType.TRUE],
    ["var", TokenType.VAR],
    ["while", TokenType.WHILE],
    ["var", TokenType.VAR]
])("%s", (source: string, expected: TokenType) => {
  const scanner = new Scanner(source);
  const tokens = scanner.scanTokens();
  expect(tokens.length).toBe(2);
  expect(tokens[0].tokenType).toBe(expected);
});
