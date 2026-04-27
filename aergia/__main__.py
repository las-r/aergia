import argparse
import subprocess
import sys
from .lexer import tokenize
from .parser import parse, ExitException

# aergia main
# made by las-r on github

def main():
    # constants
    VER = "Aergia v1.5.0"
    REPO = "git+https://github.com/las-r/aergia.git"
    
    # arguments
    aparser = argparse.ArgumentParser(
        prog="aergia",
        description="Aergia Language Interpreter"
    )
    aparser.add_argument("filename", nargs="?", help="the .aer file to execute")
    aparser.add_argument("--version", action="version", version=VER)
    aparser.add_argument("-d", "--debug", action="store_true", help="print tokens and abstract syntax tree")
    aparser.add_argument("-gu", "--ghupdate", action="store_true", help="update aergia to the latest version from github")
    args = aparser.parse_args()
    
    # handle update
    if args.ghupdate:
        print("Checking for updates...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", REPO])
            sys.exit(0)
        except subprocess.CalledProcessError as e:
            print(f"Update failed: {e}")
            sys.exit(1)

    # global environment
    env = {}
    
    try:
        # run file
        if args.filename:
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
            for node in ast:
                if node:
                    node.eval(env)
        
        # run repl
        else:
            print(f"{VER} REPL")
            while True:
                line = input(";> ")
                tokens = tokenize(line)
                ast = parse(tokens)
                for node in ast:
                    if node:
                        print(node.eval(env))
         
    except ExitException as e:
        sys.exit(e.value)       
    except FileNotFoundError:
        print(f"Aergia Error: File '{args.filename}' not found")
    except Exception as e:
        print(f"Aergia Error: {e}")
        

if __name__ == "__main__":
    main()