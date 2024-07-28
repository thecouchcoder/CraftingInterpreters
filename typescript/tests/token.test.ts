import { Token } from "../interpreter/token";
import { TokenType } from "../interpreter/tokenType";

test("can toString() token", () => {
  let t = new Token(TokenType.STRING, "hello", "world", 42);
  expect(t.toString()).toBe("STRING hello world");
});
