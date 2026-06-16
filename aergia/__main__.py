import argparse
import subprocess
import sys
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError
from typing import Any

from .lexer import tokenize
from .parser import parse, ExitException
from .nodes import AergiaRuntimeError

from .tools import agathos
from .tools import lethes
from .tools import otia

# aergia main
# made by las-r on github

def main():
    # load version and repo
    try:
        ver = version("aergia-lang")
        repo = "git+https://github.com/las-r/aergia"
    except PackageNotFoundError:
        ver = "development"
        repo = "local"
    
    # arguments
    aparser = argparse.ArgumentParser(
        prog="aergia", description="Aergia Language Interpreter"
    )
    aparser.add_argument("filename", nargs="?", help="the file to execute")
    aparser.add_argument("--version", action="version", version=ver)
    aparser.add_argument("-d", "--debug", action="store_true", help="print tokens and abstract syntax tree")
    aparser.add_argument("-gu", "--ghupdate", action="store_true", help="update aergia to the latest version from github")
    aparser.add_argument("-l", "--lethes", action="store_true", help="minify program")
    aparser.add_argument("-o", "--otia", action="store_true", help="prettify program")
    aparser.add_argument("-lg", "--libget", help="install a package from a github url")
    aparser.add_argument("-lr", "--librem", help="remove an installed package by name")
    aparser.add_argument("-ll", "--libls", action="store_true", help="list installed packages")
    args = aparser.parse_args()

    # handle update
    if args.ghupdate:
        print("Checking for updates...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", repo])
            sys.exit(0)
        except subprocess.CalledProcessError as e:
            print(f"Update failed: {e}")
            sys.exit(1)

    # handle lethes
    if args.lethes:
        print(f"Minifying {args.filename}...")
        try:
            lethes.minifyf(args.filename)
            sys.exit(0)
        except Exception as e:
            print(f"Lethes failed: {e}")
            sys.exit(1)
            
    # handle otia
    if args.otia:
        print(f"Prettifying {args.filename}...")
        try:
            otia.prettifyf(args.filename)
            sys.exit(0)
        except Exception as e:
            print(f"Otia failed: {e}")
            sys.exit(1)
            
    # handle agathos
    if args.libget:
        try:
            agathos.install(args.libget)
            sys.exit(0)
        except Exception as e:
            print(f"Agathos failed: {e}")
            sys.exit(1)
    if args.librem:
        try:
            agathos.remove(args.librem)
            sys.exit(0)
        except Exception as e:
            print(f"Agathos failed: {e}")
            sys.exit(1)
    if args.libls:
        try:
            agathos.listpackages()
            sys.exit(0)
        except Exception as e:
            print(f"Agathos failed: {e}")
            sys.exit(1)

    # global environment
    env: dict[str, Any] = {
        "__stdlib__": Path(__file__).parent / "std",
        "__lib__": Path(__file__).parent / "lib"
    }
    
    try:
        # run file
        if args.filename:
            # read file
            with open(args.filename, "r") as f:
                code = f.read()

            # path
            env["__dir__"] = Path(args.filename).parent

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
            print(f"{ver} REPL")
            env["__dir__"] = Path.cwd()
            while True:
                try:
                    line = input(";> ")
                    tokens = tokenize(line)
                    ast = parse(tokens)
                    for node in ast:
                        if node:
                            print(node.eval(env))
                except EOFError:
                    print("\nExiting REPL...")
                    break
                except KeyboardInterrupt:
                    print("KeyboardInterrupt (Type ~> 0 to exit)")
                except ExitException as e:
                    print(f"Exiting with code {e.value}...")
                    sys.exit(e.value)
                except AergiaRuntimeError as e:
                    print(f"Aergia Runtime Error: {e.message}")
                except Exception as e:
                    print(f"Fatal Aergia Interpreter Error: {e}")
    
    # error catching
    except ExitException as e:
        sys.exit(e.value)
    except FileNotFoundError:
        print(f"Aergia Error: File '{args.filename}' not found")
        sys.exit(1)
    except AergiaRuntimeError as e:
        print(f"Aergia Runtime Error [Line {e.line}, Col {e.col}]: {e.message}")
        if args.filename and e.line:
            try:
                with open(args.filename, "r") as f:
                    lines = f.readlines()
                    if 0 < e.line <= len(lines):
                        error_line = lines[e.line - 1].rstrip()
                        print(f"    {error_line}")
                        print(f"    {' ' * (e.col - 1)}^")
            except Exception:
                pass
        sys.exit(1)
    except Exception as e:
        print(f"Fatal Aergia Interpreter Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
