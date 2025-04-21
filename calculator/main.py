# main.py
import sys
from calculator.parser import parse
from calculator.evaluator import evaluate

def main():
    try:
        args = sys.argv[1:]
        degrees_mode = False
        expression = None

        for arg in args:
            if arg == "--degrees":
                degrees_mode = True
            else:
                expression = arg

        if not expression:
            raise ValueError("No expression provided")

        expr = parse(expression)
        result = evaluate(expr, degrees=degrees_mode)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()
