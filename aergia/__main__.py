import sys
import aergia.lexer
import aergia.nodes
import aergia.parser

# aergia
# by las-r

def main():
    if len(sys.argv) < 2:
        print("usage: python -m aergia <file.aer>")
        return

    file = sys.argv[1]
    with open(file) as f:
        code = f.read()

    tokens = aergia.lexer.tokenize(code)
    nodes = aergia.parser.parse(tokens)
    env = {}
    for n in nodes:
        n.eval(env)
        
    print(env)

if __name__ == "__main__":
    main()