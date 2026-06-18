import argparse
import json
import linecache
import subprocess
import sys
import urllib.error
import urllib.request
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
from typing import Any

from .lexer import tokenize
from .parser import parse, ExitException
from .nodes import AergiaRuntimeError, Environment

from .tools import agathos
from .tools import lethes
from .tools import otia
 
# aergia main
# made by las-r on github

# helpers
def latestpypi(timeout=1.5):
    try:
        url = f"https://pypi.org/pypi/aergia-lang/json"
        req = urllib.request.Request(url, headers={"User-Agent": "AergiaCLI"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode())
            return data["info"]["version"]
    except (json.JSONDecodeError, urllib.error.URLError):
        return "unknown"

def verstring():
    try:
        current = version("aergia-lang")
    except PackageNotFoundError:
        current = "DEV"
    latest = latestpypi()
    return f"v{current} (PyPI: v{latest})"

def traceback(e, defaultf="<unknown>"):
    frames = getattr(e, "frames", []) or [(defaultf, e.line, e.col)]
    print("Aergia Traceback:")
    for filepath, line, col in reversed(frames):
        print(f"    \"{filepath}\", line {line}, col {col}")
        if line and filepath and filepath not in ("<dynamic code>", "<repl>"):
            errline = linecache.getline(str(filepath), line).rstrip()
            if errline:
                print(f"        {errline}")
                print(f"        {' ' * (col - 1)}^")
    print(f"Aergia Runtime Error [Line {e.line}, Col {e.col}]: {e.message}")

# argparse actions
class CustomVersion(argparse.Action):
    def __init__(self, **kwargs):
        super().__init__(nargs=0, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        print(verstring())
        sys.exit(0)

# main
def main():
    # load version and repo
    try:
        ver = version("aergia-lang")
        repo = "git+https://github.com/las-r/aergia"
    except PackageNotFoundError:
        ver = "DEV"
        repo = "LOCAL"
    
    # arguments
    aparser = argparse.ArgumentParser(
        prog="aergia", description="Aergia Language Interpreter"
    )
    aparser.add_argument("filename", nargs="?", help="the file to execute")
    aparser.add_argument("-v", "--version", action=CustomVersion, help="show program's version number and exit")
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
    env = Environment({
        "__stdlib__": Path(__file__).parent / "std",
        "__lib__": Path(__file__).parent / "lib"
    })
    
    try:
        # run file
        if args.filename:
            # read file
            with open(args.filename, "r") as f:
                code = f.read()

            # path
            env["__file__"] = Path(args.filename).resolve()
            env["__dir__"] = env["__file__"].parent

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
            env["__file__"] = "<repl>"
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
                    traceback(e, defaultf="<repl>")
                except Exception as e:
                    print(f"Fatal Aergia Interpreter Error: {e}")
    
    # error catching
    except ExitException as e:
        sys.exit(e.value)
    except FileNotFoundError:
        print(f"Aergia Error: File '{args.filename}' not found")
        sys.exit(1)
    except AergiaRuntimeError as e:
        traceback(e, defaultf=args.filename)
        sys.exit(1)
    except Exception as e:
        print(f"Fatal Aergia Interpreter Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()