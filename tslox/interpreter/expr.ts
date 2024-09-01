import {Token} from "./token";

export type Expr = Binary | Grouping | Literal | Unary

export class Binary {
    constructor(public left: Expr, public operator: Token, public right: Expr){}

    public accept<T>(visitor: Visitor<T>): T{
        return visitor.visitBinaryExpr(this);
    }
}

export class Grouping {
    constructor(public expression: Expr){}

    public accept<T>(visitor: Visitor<T>): T{
        return visitor.visitGroupingExpr(this);
    }
}

export class Literal {
    constructor(public value: Object){}

    public accept<T>(visitor: Visitor<T>): T{
        return visitor.visitLiteralExpr(this);
    }
}

export class Unary {
    constructor(public operator: Token, public right: Expr){}

    public accept<T>(visitor: Visitor<T>): T{
        return visitor.visitUnaryExpr(this);
    }
}

export interface Visitor<T> {
    visitBinaryExpr(expr: Binary): T
    visitGroupingExpr(expr: Grouping): T
    visitLiteralExpr(expr: Literal): T
    visitUnaryExpr(expr: Unary): T
}
