import argparse
import subprocess
import sys
import tomllib
from pathlib import Path

from .lexer import tokenize
from .parser import parse, ExitException
from .nodes import *
from .tools.lethes import minifyf
from .tools.otia import prettifyf

# aergia main
# made by las-r on github


def main():
    # load toml
    mdir = Path(__file__).parent.parent
    pyprojpath = mdir / "pyproject.toml"
    with open(pyprojpath, "rb") as f:
        pyproj = tomllib.load(f)
    VER = pyproj["project"]["version"]
    REPO = f"git+{pyproj['project']['urls']['Homepage']}.git"

    # arguments
    aparser = argparse.ArgumentParser(
        prog="aergia", description="Aergia Language Interpreter"
    )
    aparser.add_argument("filename", nargs="?", help="the file to execute")
    aparser.add_argument("--version", action="version", version=VER)
    aparser.add_argument("-d", "--debug", action="store_true", help="print tokens and abstract syntax tree")
    aparser.add_argument("-gu", "--ghupdate", action="store_true", help="update aergia to the latest version from github")
    aparser.add_argument("-l", "--lethes", action="store_true", help="tool to minify program")
    aparser.add_argument("-o", "--otia", action="store_true", help="tool to prettify program")
    args = aparser.parse_args()

    # handle update
    if args.ghupdate:
        print("Checking for updates...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--upgrade", REPO]
            )
            sys.exit(0)
        except subprocess.CalledProcessError as e:
            print(f"Update failed: {e}")
            sys.exit(1)

    # handle lethes
    if args.lethes:
        print(f"Minifying {args.filename}...")
        try:
            minifyf(args.filename)
            sys.exit(0)
        except Exception as e:
            print(f"Lethes failed: {e}")
            sys.exit(1)
            
    # handle otia
    if args.otia:
        print(f"Prettifying {args.filename}...")
        try:
            prettifyf(args.filename)
            sys.exit(0)
        except Exception as e:
            print(f"Otia failed: {e}")
            sys.exit(1)
    
    # define inbuilt functions
    def in_arr(arr, itm):
        return 1 if itm in arr else 0

    # global environment
    env = {
        "in_arr": in_arr,
    }
    
    try:
        # run file
        if args.filename:
            # read file
            with open(args.filename, "r") as f:
                code = f.read()

            SOURCE_DIRECTORY = Path(args.filename).parent
            env["__dir__"] = SOURCE_DIRECTORY

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
            env["__dir__"] = Path.cwd()
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
