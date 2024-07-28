import fs from "node:fs";
import * as readline from "node:readline";
import { Scanner } from "./interpreter/scanner";
import { hadError, resetError } from "./interpreter/errorReporter";

function main() {
  if (process.argv.length > 3) {
    console.error("Usage: jlox [script]");
    return 0;
  } else if (process.argv.length == 3) {
    runFile(process.argv[2]);
  } else {
    runPrompt();
  }
}

function runFile(fileName: string) {
  // For a larger file we would want to use streams
  fs.readFile(fileName, "utf-8", (err, data) => {
    if (err) {
      console.error(err);
      return;
    }

    run(data);
    if (hadError) {
      return;
    }
  });
}

function runPrompt() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  rl.setPrompt(">");
  rl.prompt();
  rl.on("line", (line) => {
    run(line);
    rl.prompt();
    resetError();
  });
}

function run(source: string) {
  let scanner = new Scanner(source);
  let tokens = scanner.scanTokens();
  console.log(tokens);
}

main();
