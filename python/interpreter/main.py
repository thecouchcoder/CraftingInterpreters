import sys

from error_reporter import ErrorReporter
from scanner import Scanner


def run_file(file_name: str):
    with open(file_name, mode='r') as file:
        source = file.read()
    run(source)
    if errorReporter.had_error:
        exit(1)
    return


def run_prompt():
    while True:
        source = input("> ")
        run(source)
        errorReporter.had_error = False


def run(source: str):
    s = Scanner(source, errorReporter)
    tokens = s.scan_tokens()
    print(tokens)


errorReporter = ErrorReporter()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        print("Usage: jlox [script]")
        exit(1)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()
