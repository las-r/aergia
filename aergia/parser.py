from aergia.lexer import Tokens
from aergia.nodes import *

# aergia parser
# by las-r

# math parser
def parsem(tokens: Tokens):
    tok = tokens.peek()
    if tok and tok.value in UNOPS:
        op = tokens.eat().value
        a = parsex(tokens)
        return UnOpNode(op, a)
    if tok and tok.value in BINOPS:
        op = tokens.eat().value
        a = parsex(tokens)
        b = parsex(tokens)
        return BinOpNode(op, a, b)
    return None

# expression parser
def parsex(tokens: Tokens):
    tok = tokens.peek()
    if tok is None:
        raise SyntaxError("Unexpected end of input")

    # assignment
    if tok == "=":
        tokens.eat()
        name = tokens.eat().value
        value = parsex(tokens)
        return AssignNode(name, value)

    # math
    if tok in UNOPS or tok in BINOPS:
        return parsem(tokens)

    # literals & identifiers
    tok = tokens.eat()
    if len(tok) > 1 and tok[0] == tok[-1] == '"':
        return LiteralNode(tok[1:-1])
    try:
        return LiteralNode(int(tok))
    except ValueError:
        try:
            return LiteralNode(float(tok))
        except ValueError:
            return IdentifierNode(tok)

# main parser
def parse(tokens: Tokens):
    nodes = []
    while tokens.can_eat():
        nodes.append(parsex(tokens))
    return nodes