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
    token, line, col = tokens.pop(0)
    
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
        if tokens: tokens.pop(0)
        elsebody = []
        if tokens and tokens[0][0] == "->":
            tokens.pop(0)
            if tokens and tokens[0][0] == "(":
                tokens.pop(0)
                while tokens and tokens[0][0] != ")":
                    elsebody.append(parseexpr(tokens))
                if tokens: tokens.pop(0)
            else:
                raise SyntaxError("Expected '(' after '->' operator")
        return track(IfNode(cond, body, elsebody))
    
    # while/for block
    if token == "[":
        if tokens and tokens[0][0] == "`":
            tokens.pop(0)
            array = parseexpr(tokens)
            iname = tokens.pop(0)[0]
            body = []
            while tokens and tokens[0][0] != "]":
                body.append(parseexpr(tokens))
            if tokens: tokens.pop(0)
            return track(ForNode(array, iname, body))
        else:
            cond = parseexpr(tokens)
            body = []
            while tokens and tokens[0][0] != "]":
                body.append(parseexpr(tokens))
            if tokens: tokens.pop(0)
            return track(WhileNode(cond, body))
    
    # function block
    if token == "{":
        name = tokens.pop(0)[0]
        para = []
        if tokens and tokens[0][0] == ":":
            tokens.pop(0)
            while tokens and tokens[0][0] != ":":
                para.append(tokens.pop(0)[0])
            if tokens: tokens.pop(0)
        body = []
        while tokens and tokens[0][0] != "}":
            body.append(parseexpr(tokens))
        if tokens: tokens.pop(0)
        return track(FunctionNode(name, para, body))
    
    # array definition
    if token == "<":
        elements = []
        while tokens and tokens[0][0] != ">":
            elements.append(parseexpr(tokens))
        if tokens: tokens.pop(0)
        return track(ArrayNode(elements))
    
    # other array tokens
    if token == ":":
        array = parseexpr(tokens)
        index = parseexpr(tokens)
        return track(IndexNode(array, index))
    if token == "+:":
        array = parseexpr(tokens)
        item = parseexpr(tokens)
        return track(PushNode(array, item))
    if token == "-:":
        array = parseexpr(tokens)
        return track(PopNode(array))
    if token == "~:":
        array = parseexpr(tokens)
        index = parseexpr(tokens)
        return track(PopIndexNode(array, index))
    if token == "*:":
        array = parseexpr(tokens)
        index = parseexpr(tokens)
        item = parseexpr(tokens)
        return track(InsertNode(array, item, index))
    if token == "#:":
        array = parseexpr(tokens)
        item = parseexpr(tokens)
        return track(RemoveItemNode(array, item))
    if token == "::":
        array = parseexpr(tokens)
        start = parseexpr(tokens)
        end = parseexpr(tokens)
        return track(SliceNode(array, start, end))
    if token == "=:":
        array = parseexpr(tokens)
        index = parseexpr(tokens)
        value = parseexpr(tokens)
        return track(SetIndexNode(array, index, value))
    
    # exit
    if token == "~>":
        value = parseexpr(tokens)
        return track(ExitNode(value))
    
    # imports
    if token == "+>":
        file = parseexpr(tokens)
        return track(ImportNode(file))
    if token == "*>":
        name = tokens.pop(0)[0]
        return track(PyImportNode(name, name, False))
    if token == "*<":
        name = tokens.pop(0)[0]
        rname = tokens.pop(0)[0]
        return track(PyImportNode(name, rname, True))
    
    # evaluation
    if token == ";":
        value = parseexpr(tokens)
        return track(EvaluationNode(value))
    
    # assignments
    if token == "=":
        if tokens and tokens[0][0] in BINOPS:
            op = tokens.pop(0)[0]
            vname = tokens[0][0]
            vval = parseexpr(tokens)
            value = parseexpr(tokens)
            if op == "&&":
                return track(AssignNode(vname, track(ShortCircuitANDNode(vval, value))))
            if op == "||":
                return track(AssignNode(vname, track(ShortCircuitORNode(vval, value))))
            return track(AssignNode(vname, track(BinaryOpNode(op, vval, value))))
        if tokens and tokens[0][0] in UNOPS:
            op = tokens.pop(0)[0]
            vname = tokens[0][0]
            vval = parseexpr(tokens)
            return track(AssignNode(vname, track(UnaryOpNode(op, vval))))
        name = tokens.pop(0)[0]
        val = parseexpr(tokens)
        return track(AssignNode(name, val))
    
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
    
    # function return
    if token == "?": return track(ReturnNode(parseexpr(tokens)))
    
    # function call
    if token == "@":
        name = tokens.pop(0)[0]
        args = []
        if tokens and tokens[0][0] == ":":
            tokens.pop(0)
            while tokens and tokens[0][0] != ":":
                args.append(parseexpr(tokens))
            if tokens: tokens.pop(0)
        return track(CallNode(name, args))
    
    # string
    if token.startswith('"'):
        content = token[1:-1]
        unescaped = re.sub(r'\\(.)', r'\1', content)
        return track(LiteralNode(unescaped))
    
    # number and variable
    try:
        val = float(token)
        return track(LiteralNode(int(val) if val.is_integer() else val))
    except ValueError:
        return track(VariableNode(token))

# tree maker
def parse(tokens):
    ast = []
    while tokens:
        node = parseexpr(tokens)
        if node:
            ast.append(node)
    return ast