import {Binary, Expr, Grouping, Literal, Unary, Visitor} from "./expr";

export class AstPrinter implements Visitor<string> {

    print(expr: Expr): string {
        return expr.accept(this);
    }

    parenthesize(name: string, ...exprs: Expr[]): string {
        let s = "";
        s += `(${name}`;
        exprs.forEach(expr => {
            s += " ";
            s += expr.accept(this);
        });
        s += ")";
        return s;
    }

    visitBinaryExpr(expr: Binary) {
        return this.parenthesize(expr.operator.lexeme, expr.left, expr.right);
    }

    visitGroupingExpr(expr: Grouping) {
        return this.parenthesize("group", expr.expression);

    }

    visitLiteralExpr(expr: Literal) {
        if (expr.value == null) return "nil";
        return expr.value.toString();
    }

    visitUnaryExpr(expr: Unary) {
        return this.parenthesize(expr.operator.lexeme, expr.right);
    }
}