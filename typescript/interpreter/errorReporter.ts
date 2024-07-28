export let hadError = false;

export function resetError() {
  hadError = false;
}

export function reportError(line: number, message: string) {
  report(line, "", message);
}

function report(line: number, where: string, message: string) {
  console.error(`[line ${line}] Error ${where}: ${message}`);
  hadError = true;
}
