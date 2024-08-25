import * as fs from 'fs';

defineAst("", "Expr", [
    "Binary   : Expr left, Token operator, Expr right",
    "Grouping : Expr expression",
    "Literal  : Object value",
    "Unary    : Token operator, Expr right"]);

function defineAst(outputDir: string, baseName: string, types: string[]) {
    let data = '';
    data += "import {Token} from \"./token\";";
    data += "\n\n";
    // data += `export abstract class ${baseName} {}`;
    let typeNames: string[] = [];
    types.forEach(t => {
        typeNames.push(t.split(":")[0].trim());
    });
    data += `export type ${baseName} = ${typeNames.join(" | ")}`;
    data += `\n\n`;

    for (const t of types) {
        const className = t.split(":")[0].trim();
        const fields = t.split(":")[1].trim();
        data = defineType(data, baseName, className, fields);
    }

    data = defineVisitor(data, baseName, types);

    fs.writeFileSync(`./interpreter/${baseName.toLowerCase()}.ts`, data, {encoding: 'utf8', flag: 'w'});
    console.log('File written successfully.');
}

function defineType(data: string, baseName: string, className: string, fieldsStr: string): string {
    // data += `export class ${className} extends ${baseName} {\n`;
    data += `export class ${className} {\n`;
    data += `    constructor(`;
    const fields = fieldsStr.split(',');
    for (const f of fields) {
        const id = f.trim().split(" ")[1];
        const t = f.trim().split(" ")[0];
        data += `public ${id}: ${t}, `;
    }

    data = data.substring(0, data.length - 2);
    // data += `){ super() }\n`;
    data += `){}\n`;
    data += `\n`;
    data += `    public accept<T>(visitor: Visitor<T>): T{\n`;
    data += `        return visitor.visit${className}${baseName}(this);\n`;
    data += `    }\n`;
    data += `}`;
    data += "\n\n";
    return data;
}

function defineVisitor(data: string, baseName: string, types: string[]): string {
    data += `export interface Visitor<T> {\n`;
    types.forEach((type: string) => {
        const className = type.split(":")[0].trim();
        data += `    visit${className}${baseName}(${baseName.toLowerCase()}: ${className}): T\n`;
    });
    data += `}\n`;
    return data;
}




