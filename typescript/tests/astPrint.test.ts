import {Binary, Grouping, Literal, Unary} from "../interpreter/expr";
import {TokenType} from "../interpreter/tokenType";
import {Token} from "../interpreter/token";
import {AstPrinter} from "../interpreter/astPrinter";

test("can print ast", () => {
    const expression = new Binary(
        new Unary(
            new Token(TokenType.MINUS, "-", null, 1),
            new Literal(123)),
        new Token(TokenType.STAR, "*", null, 1),
        new Grouping(new Literal(45.67))
    );

    const res = new AstPrinter().print(expression);
    expect(res).toBe("(* (- 123) (group 45.67))");
});