import argparse

def runFile(f):
	print("Running " + f)

def runPrompt():
	print("Running prompt")

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--f")
	args = parser.parse_args()
	if args.f:
		runFile(args.f)
	else:
		runPrompt()

main()
