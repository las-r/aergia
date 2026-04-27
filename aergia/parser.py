import re
from .nodes import *

# aergia parser
# made by las-r on github

# expression parser
def parseexpr(tokens):
    if not tokens:
        return None
    token = tokens.pop(0)
    
    # if block
    if token == "(":
        cond = parseexpr(tokens)
        body = []
        while tokens and tokens[0] != ")":
            body.append(parseexpr(tokens))
        if tokens: tokens.pop(0)
        elsebody = []
        if tokens and tokens[0] == "(":
            tokens.pop(0)
            while tokens and tokens[0] != ")":
                elsebody.append(parseexpr(tokens))
            if tokens: tokens.pop(0)
        return IfNode(cond, body, elsebody)
    
    # while block
    if token == "[":
        cond = parseexpr(tokens)
        body = []
        while tokens and tokens[0] != "]":
            body.append(parseexpr(tokens))
        if tokens: tokens.pop(0)
        return WhileNode(cond, body)
    
    # function block
    if token == "{":
        name = tokens.pop(0)
        para = []
        if tokens and tokens[0] == ":":
            tokens.pop(0)
            while tokens and tokens[0] != ":":
                para.append(tokens.pop(0))
            if tokens: tokens.pop(0)
        body = []
        while tokens and tokens[0] != "}":
            body.append(parseexpr(tokens))
        if tokens: tokens.pop(0)
        return FunctionNode(name, para, body)
    
    # exit
    if token == "```":
        value = parseexpr(tokens)
        return ExitNode(value)
    
    # imports
    if token == "+>":
        file = parseexpr(tokens)
        return ImportNode(file)
    if token == "*>":
        name = tokens.pop(0)
        return PyImportNode(name, False)
    if token == "*<":
        name = tokens.pop(0)
        return PyImportNode(name, True)
    
    # evaluation
    if token == ";":
        value = parseexpr(tokens)
        return EvaluationNode(value)
    
    # assignments
    if token == "=":
        name = tokens.pop(0)
        value = parseexpr(tokens)
        return AssignNode(name, value)
    
    # binary ops
    if token in ("+", "-", "*", "/", "==", "!=", ">>", "<<", ">=", "<=", "^", "%", "&", "|", "$"):
        left = parseexpr(tokens)
        right = parseexpr(tokens)
        return BinaryOpNode(token, left, right)
    
    # unary ops and output
    if token in ("!", "~", ">"):
        child = parseexpr(tokens)
        if token == ">": return OutputNode(child)
        return UnaryOpNode(token, child)
    
    # input
    if token == ".": return IntInputNode()
    if token == ",": return StringInputNode()
    if token == "'": return FloatInputNode()
    
    # function return
    if token == "?": return ReturnNode(parseexpr(tokens))
    
    # function call
    if token == "@":
        name = tokens.pop(0)
        args = []
        if tokens and tokens[0] == ":":
            tokens.pop(0)
            while tokens and tokens[0] != ":":
                args.append(parseexpr(tokens))
            if tokens: tokens.pop(0)
        return CallNode(name, args)
    
    # string
    if token.startswith('"'):
        content = token[1:-1]
        unescaped = re.sub(r'\\(.)', r'\1', content)
        return LiteralNode(unescaped)
    
    # number and variable
    try:
        val = float(token)
        return LiteralNode(int(val) if val.is_integer() else val)
    except ValueError:
        return VariableNode(token)

# tree maker
def parse(tokens):
    ast = []
    while tokens:
        node = parseexpr(tokens)
        if node:
            ast.append(node)
    return ast