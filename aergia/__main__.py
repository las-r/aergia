import argparse
from .lexer import tokenize
from .parser import parse

# aergia main
# made by las-r on github

def main():
    # arguments
    aparser = argparse.ArgumentParser(
        prog="aergia",
        description="Aergia Language Interpreter"
    )
    aparser.add_argument("filename", help="The .aer file to execute")
    aparser.add_argument("--version", action="version", version="Aergia v1.4.0")
    aparser.add_argument("-d", "--debug", action="store_true", help="print tokens and abstract syntax tree")
    args = aparser.parse_args()

    try:
        # read file
        with open(args.filename, "r") as f:
            code = f.read()
        
        # create tokens and tree
        tokens = tokenize(code)
        ast = parse(tokens)
        
        # debug
        if args.debug:
            print(f"DEBUG - Tokens: {tokens}")
            print(f"DEBUG - AST: {ast}")
        
        # interpret
        env = {}
        for node in ast:
            if node:
                node.eval(env)
                
    except FileNotFoundError as e:
        print(f"Aergia Error: File '{args.filename}' not found")
    except Exception as e:
        print(f"Aergia Error: {e}")

if __name__ == "__main__":
    main()