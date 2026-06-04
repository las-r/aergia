import re
from .nodes import *

# aergia parser
# made by las-r on github

# constants
BINOPS = ["+", "-", "*", "/", "==", "!=", ">>", "<<", ">=", "<=", "^", "%", "&", "|", "$", "&&", "||"]
UNOPS = ["!", "~"]

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
    
    # while/for block
    if token == "[":
        if tokens and tokens[0] == "`":
            tokens.pop(0)
            array = parseexpr(tokens)
            iname = tokens.pop(0)
            body = []
            while tokens and tokens[0] != "]":
                body.append(parseexpr(tokens))
            if tokens: tokens.pop(0)
            return ForNode(array, iname, body)
        else:
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
    
    # array definition
    if token == "<":
        elements = []
        while tokens and tokens[0] != ">":
            elements.append(parseexpr(tokens))
        if tokens: tokens.pop(0)
        return ArrayNode(elements)
    
    # other array tokens
    if token == ":":
        array = parseexpr(tokens)
        index = parseexpr(tokens)
        return IndexNode(array, index)
    if token == "+:":
        array = parseexpr(tokens)
        item = parseexpr(tokens)
        return PushNode(array, item)
    if token == "-:":
        array = parseexpr(tokens)
        return PopNode(array)
    if token == "~:":
        array = parseexpr(tokens)
        index = parseexpr(tokens)
        return PopIndexNode(array, index)
    if token == "*:":
        array = parseexpr(tokens)
        index = parseexpr(tokens)
        item = parseexpr(tokens)
        return InsertNode(array, item, index)
    if token == "#:":
        array = parseexpr(tokens)
        item = parseexpr(tokens)
        return RemoveItemNode(array, item)
    if token == "::":
        array = parseexpr(tokens)
        start = parseexpr(tokens)
        end = parseexpr(tokens)
        return SliceNode(array, start, end)
    
    # exit
    if token == "~>":
        value = parseexpr(tokens)
        return ExitNode(value)
    
    # imports
    if token == "+>":
        file = parseexpr(tokens)
        return ImportNode(file)
    if token == "*>":
        name = tokens.pop(0)
        return PyImportNode(name, name, False)
    if token == "*<":
        name = tokens.pop(0)
        rname = tokens.pop(0)
        return PyImportNode(name, rname, True)
    
    # evaluation
    if token == ";":
        value = parseexpr(tokens)
        return EvaluationNode(value)
    
    # assignments
    if token == "=":
        if tokens and tokens[0] in BINOPS:
            op = tokens.pop(0)
            vname = tokens[0]
            vval = parseexpr(tokens)
            value = parseexpr(tokens)
            if op == "&&":
                return AssignNode(vname, ShortCircuitANDNode(vval, value))
            if op == "||":
                return AssignNode(vname, ShortCircuitORNode(vval, value))
            return AssignNode(vname, BinaryOpNode(op, vval, value))
        if tokens and tokens[0] in UNOPS:
            op = tokens.pop(0)
            vname = tokens[0]
            vval = parseexpr(tokens)
            return AssignNode(vname, UnaryOpNode(op, vval))
        name = tokens.pop(0)
        val = parseexpr(tokens)
        return AssignNode(name, val)
    
    # binary ops
    if token in BINOPS:
        if token == "&&":
            left = parseexpr(tokens)
            right = parseexpr(tokens)
            return ShortCircuitANDNode(left, right)
        if token == "||":
            left = parseexpr(tokens)
            right = parseexpr(tokens)
            return ShortCircuitORNode(left, right)
        left = parseexpr(tokens)
        right = parseexpr(tokens)
        return BinaryOpNode(token, left, right)
    
    # unary ops and output
    if token in UNOPS:
        left = parseexpr(tokens)
        return UnaryOpNode(token, left)
    
    # output
    if token == ">": 
        child = parseexpr(tokens)
        return OutputNode(child)
    
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