import re
from collections import deque

from .nodes import *

# aergia parser
# made by las-r on github

# arithmetic and logical operators
BINOPS = ["+", "-", "*", "/", "==", "!=", ">>", "<<", ">=", "<=", "^", "%", "&", "|", "$", "&&", "||"]
UNOPS = ["!", "~"]

# array operators
ARROPS = {
    ":": (IndexNode, 2),
    "+:": (PushNode, 2),
    "-:": (PopNode, 1),
    "~:": (PopIndexNode, 2),
    "*:": (lambda a, idx, itm: InsertNode(a, itm, idx), 3), # Reorder parameter structure layout
    "$:": (RemoveItemNode, 2),
    "::": (SliceNode, 3),
    "=:": (SetIndexNode, 3)
}

# expression parser
def parseexpr(tokens):
    if not tokens:
        return None
    token, line, col = tokens.popleft()
    
    # tracking helper
    def track(node):
        node.line = line
        node.col = col
        return node
    
    # if block
    if token == "(":
        cond = parseexpr(tokens)
        body = []
        while tokens and tokens[0][0] != ")":
            body.append(parseexpr(tokens))
        if tokens: tokens.popleft()
        elsebody = []
        if tokens and tokens[0][0] == "->":
            tokens.popleft()
            if tokens and tokens[0][0] == "(":
                tokens.popleft()
                while tokens and tokens[0][0] != ")":
                    elsebody.append(parseexpr(tokens))
                if tokens: tokens.popleft()
            else:
                raise SyntaxError("Expected '(' after '->' operator")
        return track(IfNode(cond, body, elsebody))
    
    # while/for block
    if token == "[":
        if tokens and tokens[0][0] == "`":
            tokens.popleft()
            array = parseexpr(tokens)
            iname = tokens.popleft()[0]
            body = []
            while tokens and tokens[0][0] != "]":
                body.append(parseexpr(tokens))
            if tokens: tokens.popleft()
            return track(ForNode(array, iname, body))
        else:
            cond = parseexpr(tokens)
            body = []
            while tokens and tokens[0][0] != "]":
                body.append(parseexpr(tokens))
            if tokens: tokens.popleft()
            return track(WhileNode(cond, body))
    
    # function block
    if token == "{":
        if tokens and tokens[0][0] == ":":
            tokens.popleft()
            para = []
            while tokens and tokens[0][0] != ":":
                para.append(tokens.popleft()[0])
            if tokens: tokens.popleft()
            body = []
            while tokens and tokens[0][0] != "}":
                body.append(parseexpr(tokens))
            if tokens: tokens.popleft()
            return track(AnonymousFunctionNode(para, body))
        else:
            name = tokens.popleft()[0]
            para = []
            if tokens and tokens[0][0] == ":":
                tokens.popleft()
                while tokens and tokens[0][0] != ":":
                    para.append(tokens.popleft()[0])
                if tokens: tokens.popleft()
            body = []
            while tokens and tokens[0][0] != "}":
                body.append(parseexpr(tokens))
            if tokens: tokens.popleft()
            return track(FunctionNode(name, para, body))
    
    # arrays
    if token == "<":
        elements = []
        while tokens and tokens[0][0] != ">":
            elements.append(parseexpr(tokens))
        if tokens: tokens.popleft()
        return track(ArrayNode(elements))
    if token in ARROPS:
        node, arity = ARROPS[token]
        args = [parseexpr(tokens) for _ in range(arity)]
        return track(node(*args))
    
    # range
    if token == "..":
        start = parseexpr(tokens)
        end = parseexpr(tokens)
        inc = parseexpr(tokens)
        return track(RangeNode(start, end, inc))
    
    # imports
    if token == "+>":
        file = parseexpr(tokens)
        return track(ImportNode(file, None, False))
    if token == "+<":
        file = parseexpr(tokens)
        rname = rname = tokens.popleft()[0]
        return track(ImportNode(file, rname, True))
    if token == "*>":
        name = tokens.popleft()[0]
        return track(PyImportNode(name, name, False))
    if token == "*<":
        name = tokens.popleft()[0]
        rname = tokens.popleft()[0]
        return track(PyImportNode(name, rname, True))
    
    # exit
    if token == "~>":
        value = parseexpr(tokens)
        return track(ExitNode(value))
    
    # evaluation
    if token == ";":
        value = parseexpr(tokens)
        return track(EvaluationNode(value))
    
    # assignments
    if token == "=":
        if tokens and tokens[0][0] in BINOPS:
            op = tokens.popleft()[0]
            vname = tokens[0][0]
            vval = parseexpr(tokens)
            value = parseexpr(tokens)
            if op == "&&":
                return track(AssignNode(vname, track(ShortCircuitANDNode(vval, value))))
            if op == "||":
                return track(AssignNode(vname, track(ShortCircuitORNode(vval, value))))
            return track(AssignNode(vname, track(BinaryOpNode(op, vval, value))))
        if tokens and tokens[0][0] in UNOPS:
            op = tokens.popleft()[0]
            vname = tokens[0][0]
            vval = parseexpr(tokens)
            return track(AssignNode(vname, track(UnaryOpNode(op, vval))))
        name = tokens.popleft()[0]
        val = parseexpr(tokens)
        return track(AssignNode(name, val))
    
    # super assignment
    if token == "=?":
        name = tokens.popleft()[0]
        cons = parseexpr(tokens)
        return track(SuperNode(name, cons))
    
    # binary ops
    if token in BINOPS:
        if token == "&&":
            left = parseexpr(tokens)
            right = parseexpr(tokens)
            return track(ShortCircuitANDNode(left, right))
        if token == "||":
            left = parseexpr(tokens)
            right = parseexpr(tokens)
            return track(ShortCircuitORNode(left, right))
        left = parseexpr(tokens)
        right = parseexpr(tokens)
        return track(BinaryOpNode(token, left, right))
    
    # unary ops and output
    if token in UNOPS:
        left = parseexpr(tokens)
        return track(UnaryOpNode(token, left))
    
    # output
    if token == ">": 
        child = parseexpr(tokens)
        return track(OutputNode(child))
    
    # input
    if token == ".": return track(IntInputNode())
    if token == ",": return track(StringInputNode())
    if token == "'": return track(FloatInputNode())
    
    # break and continue
    if token == "<<<": return track(BreakNode())
    if token == ">>>": return track(ContinueNode())
    
    # function return
    if token == "?": return track(ReturnNode(parseexpr(tokens)))
    
    # function call
    if token == "@":
        target = parseexpr(tokens)
        args = []
        if tokens and tokens[0][0] == ":":
            tokens.popleft()
            while tokens and tokens[0][0] != ":":
                args.append(parseexpr(tokens))
            if tokens: tokens.popleft()
        return track(CallNode(target, args))
    
    # string
    if token.startswith('"'):
        content = token[1:-1]
        unescaped = re.sub(r'\\(.)', r'\1', content)
        return track(LiteralNode(unescaped))
    
    # number and variable
    clean = '-' + token[1:] if token.startswith('_') and len(token) > 1 else token
    try:
        val = float(clean)
        return track(LiteralNode(int(val) if val.is_integer() else val))
    except ValueError:
        return track(VariableNode(token))

# tree maker
def parse(tokens):
    tokens = deque(tokens)
    ast = []
    while tokens:
        node = parseexpr(tokens)
        if node:
            ast.append(node)
    return ast