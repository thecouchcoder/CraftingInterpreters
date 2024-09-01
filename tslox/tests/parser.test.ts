import {Scanner} from "../interpreter/scanner";
import {Parser} from "../interpreter/parser";
import {AstPrinter} from "../interpreter/astPrinter";

describe("can print", () => {
    it.each([
        ["5+3", "(+ 5 3)"],
        ["10-2*4", "(- 10 (* 2 4))"],
        ["5>3", "(> 5 3)"],
        ["5+3 != 8", "(!= (+ 5 3) 8)"],
        ["!4", "(! 4)"],
        ["-(5>3) == !false", "(== (- (group (> 5 3))) (! false))"]
    ])("when source is '%s", (text, expected) => {
        const scanner = new Scanner(text);
        const tokens = scanner.scanTokens();
        const parser = new Parser(tokens);
        const expr = parser.parse();
        const result = new AstPrinter().print(expr);
        expect(result).toBe(expected);
    });
});