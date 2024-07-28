function main() {
  console.log(process.argv);
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
  console.log(`Running ${fileName}`);
}

function runPrompt() {
  console.log("Running prompt");
}

main();
