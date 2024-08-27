import {Token} from "./token";
import {TokenType} from "./tokenType";

export let hadError = false;

export function resetError() {
    hadError = false;
}

export function reportError(line: number, message: string) {
    report(line, "", message);
}

export function error(token: Token, message: string) {
    if (token.tokenType == TokenType.EOF) {
        report(token.line, " at end", message);
    } else {
        report(token.line, " at '" + token.lexeme + "'", message);
    }
}

function report(line: number, where: string, message: string) {
    console.error(`[line ${line}] Error ${where}: ${message}`);
    hadError = true;
}