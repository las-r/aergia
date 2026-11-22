import re
from aergia.lexer import Tokens
from aergia.nodes import *

# aergia parser
# by las-r

# body parser
def parseb(tokens: Tokens, end):
    body = []
    while tokens.can_eat() and tokens.peek() != end:
        body.append(parsex(tokens))
    tokens.expect(end)
    return body

# expression parser
def parsex(tokens: Tokens):
    tok = tokens.peek()
    if tok is None:
        raise SyntaxError("Unexpected end of input")

    # assignment
    if tok == "=":
        tokens.eat()
        name = tokens.eat()
        value = parsex(tokens)
        return AssignNode(name, value)

    # io
    if tok == ">":
        tokens.eat()
        value = parsex(tokens)
        return PrintNode(value)
    if tok == ",":
        tokens.eat()
        return InputNode(str)
    if tok == ".":
        tokens.eat()
        return InputNode(int)
    if tok == "'":
        tokens.eat()
        return InputNode(float)

    # control flow
    if tok == "(":
        tokens.eat()
        cond = parsex(tokens)
        body = parseb(tokens, ")")
        tokens.expect("(")
        ebody = parseb(tokens, ")")
        return IfNode(cond, body, ebody)
    if tok == "[":
        tokens.eat()
        cond = parsex(tokens)
        body = parseb(tokens, "]")
        return WhileNode(cond, body)

    # functional
    if tok == "{":
        tokens.eat()
        params = []
        if tokens.peek() == ":":
            tokens.eat()
            while tokens.can_eat() and tokens.peek() != ":":
                params.append(tokens.eat())
            tokens.expect(":")
        body = parseb(tokens, "}")
        return DefinitionNode(params, body)
    if tok == "@":
        tokens.eat()
        func = parsex(tokens)
        args = []
        if tokens.peek() == ":":
            tokens.eat()
            args = parseb(tokens, ":")
        return CallNode(func, args)
    if tok == "?":
        tokens.eat()
        value = parsex(tokens)
        return ReturnNode(value)

    # math
    if tok in UNOPS:
            op = tokens.eat()
            a = parsex(tokens)
            return UnOpNode(op, a)
    if tok in BINOPS:
        op = tokens.eat()
        a = parsex(tokens)
        b = parsex(tokens)
        return BinOpNode(op, a, b)

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
            if not re.compile(r"[a-zA-Z][a-zA-Z0-9]*").fullmatch(tok):
                raise SyntaxError(f"Invalid token '{tok}'")
            return IdentifierNode(tok)

# main parser
def parse(tokens: Tokens):
    nodes = []
    while tokens.can_eat():
        nodes.append(parsex(tokens))
    return nodes