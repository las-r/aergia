import re
from aergia.lexer import Tokens
from aergia.nodes import *

# aergia parser
# by las-r

# identifier checker
def check(iden):
    if not re.compile(r"[a-zA-Z][a-zA-Z0-9]*|;").fullmatch(iden):
        raise SyntaxError(f"Invalid token '{iden}'")
    return iden

# body parser
def parseb(tokens: Tokens, end):
    body = []
    while tokens.can_eat() and tokens.peek() != end:
        body.append(parsex(tokens))
    tokens.expect(end)
    return body

# expression parser
def parsex(tokens: Tokens):
    tok = tokens.eat()
    if tok is None:
        raise SyntaxError("Unexpected end of input")

    # assignment
    if tok == "=":
        name = check(tokens.eat())
        value = parsex(tokens)
        return AssignNode(name, value)

    # io
    if tok == ">":
        value = parsex(tokens)
        return PrintNode(value)
    if tok == ",":
        return InputNode(str)
    if tok == ".":
        return InputNode(int)
    if tok == "'":
        return InputNode(float)

    # control flow
    if tok == "(":
        cond = parsex(tokens)
        body = parseb(tokens, ")")
        tokens.expect("(")
        ebody = parseb(tokens, ")")
        return IfNode(cond, body, ebody)
    if tok == "[":
        cond = parsex(tokens)
        body = parseb(tokens, "]")
        return WhileNode(cond, body)

    # functional
    if tok == "{":
        params = []
        if tokens.peek() == ":":
            tokens.eat()
            while tokens.can_eat() and tokens.peek() != ":":
                params.append(tokens.eat())
            tokens.expect(":")
        body = parseb(tokens, "}")
        return DefinitionNode(params, body)
    if tok == "@":
        func = parsex(tokens)
        args = []
        if tokens.peek() == ":":
            tokens.eat()
            args = parseb(tokens, ":")
        return CallNode(func, args)
    if tok == "?":
        value = parsex(tokens)
        return ReturnNode(value)

    # math
    if tok in UNOPS:
        a = parsex(tokens)
        return UnOpNode(tok, a)
    if tok in BINOPS:
        a = parsex(tokens)
        b = parsex(tokens)
        return BinOpNode(tok, a, b)

    # literals & identifiers
    if len(tok) > 1 and tok[0] == tok[-1] == '"':
        return LiteralNode(tok[1:-1])
    try:
        return LiteralNode(int(tok))
    except ValueError:
        try:
            return LiteralNode(float(tok))
        except ValueError:
            return IdentifierNode(check(tok))

# main parser
def parse(tokens: Tokens):
    nodes = []
    while tokens.can_eat():
        nodes.append(parsex(tokens))
    return nodes