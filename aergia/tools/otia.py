import os
from ..lexer import tokenize

# aergia prettifier
# by las-r

# token stream
class TokenStream:
    def __init__(self, tokens):
        self.tokens = [t[0] for t in tokens if t and isinstance(t, tuple) and t[0].strip()]
        self.i = 0
        
    def get(self):
        if self.can_push():
            return self.tokens[self.i]
        return ""
        
    def push(self):
        token = self.get()
        self.i += 1
        return token
    
    def can_push(self):
        return self.i < len(self.tokens)

# constants
ABINOPS = ["+", "-", "*", "/", "^", "%", "&", "|", "$"]
AUNOPS = ["~"]
CBINOPS = ["==", "!=", "<<", ">>", "<=", ">=", "&&", "||"]
CUNOPS = ["!", "=,", "=.", "='"]
ZCMDS = [".", ",", "'", "<<<", ">>>"]
UCMDS = ["-:", "+>", "*>", ";", "~>", ">", "?"]
BCMDS = [":", "+:", "~:", "$:", "+<", "*<", "`", "->"]
TCMDS = ["*:", "::", "=:", "..", "=>"]
ACMDS = ["=", "=?"]
BSTART = {"(": ")", "[": "]", "{": "}"}

# functions
def parselist(stream, end, depth):
    pl = []
    while stream.can_push() and stream.get() != end:
        pl.append(prettify(stream, depth, inline=True))
    if stream.can_push() and stream.get() == end:
        stream.push()
    return " ".join(pl)

def prettify(stream, depth, inline=False):
    if not stream.can_push():
        return ""
    token = stream.push()
    res = ""
    
    # operators
    if token in ABINOPS:
        x = prettify(stream, depth, inline=True)
        y = prettify(stream, depth, inline=True)
        res = f"{token}{x} {y}"
    elif token in AUNOPS + CUNOPS:
        x = prettify(stream, depth, inline=True)
        res = f"{token}{x}"
    elif token in CBINOPS:
        x = prettify(stream, depth, inline=True)
        y = prettify(stream, depth, inline=True)
        res = f"{token} {x} {y}"
        
    # arrays
    elif token == "<":
        items = parselist(stream, ">", depth)
        res = f"< {items} >"
        
    # commands
    elif token in ZCMDS:
        res = token 
    elif token in TCMDS:
        a = prettify(stream, depth, inline=True)
        b = prettify(stream, depth, inline=True)
        c = prettify(stream, depth, inline=True)
        res = f"{token} {a} {b} {c}"
    elif token in BCMDS:
        a = prettify(stream, depth, inline=True)
        b = prettify(stream, depth, inline=True)
        res = f"{token} {a} {b}"
    elif token in UCMDS:
        a = prettify(stream, depth, inline=True)
        res = f"{token} {a}"
        
    # assignments
    elif token in ACMDS:
        a = prettify(stream, depth, inline=True)
        if a in ABINOPS + CBINOPS:
            b = prettify(stream, depth, inline=True)
            c = prettify(stream, depth, inline=True)
            res = f"={a} {b} {c}"
        elif a in AUNOPS + CUNOPS:
            b = prettify(stream, depth, inline=True)
            res = f"={a} {b}"
        else:
            b = prettify(stream, depth, inline=True)
            res = f"= {a} {b}"
        
    # function calls
    elif token == "@":
        name = prettify(stream, depth, inline=True)
        para = ""
        if stream.can_push() and stream.get() == ":":
            stream.push()
            para = f":{parselist(stream, ':', depth)}:"
        res = f"@{name}{para}"
        
    # blocks
    elif token in BSTART:
        end = BSTART[token]
        header = ""
        if token == "{":
            name = prettify(stream, depth, inline=True)
            params = ""
            if stream.can_push() and stream.get() == ":":
                stream.push()
                params = f":{parselist(stream, ':', depth)}:"
            header = f"{name} {params}"
        elif token == "(":
            header = prettify(stream, depth, inline=True)
        elif token == "[":
            header = prettify(stream, depth, inline=True)
        body_lines = []
        while stream.can_push() and stream.get() != end:
            inner = prettify(stream, depth + 1, inline=False)
            if inner.strip():
                body_lines.append(inner)
        if stream.can_push() and stream.get() == end:
            stream.push()
        ind = " " * depth * 4
        inner_str = "".join(body_lines)
        if token == "{":
            res = f"{{{header}\n{inner_str}{ind}}}"
        else:
            res = f"{token}{header}\n{inner_str}{ind}{end}"
        if token == "(" and not inline:
            if stream.can_push() and stream.get() == "->":
                stream.push()
                if stream.can_push() and stream.get() == "(":
                    stream.push()
                    else_body_lines = []
                    while stream.can_push() and stream.get() != ")":
                        inner = prettify(stream, depth + 1, inline=False)
                        if inner.strip():
                            else_body_lines.append(inner)  
                    if stream.can_push() and stream.get() == ")":
                        stream.push()
                    elseinnerstr = "".join(else_body_lines)
                    elseblock = f"(\n{elseinnerstr}{ind})"
                else:
                    elseblock = prettify(stream, depth, inline=False).strip()
                res = f"{res.rstrip()} -> {elseblock}"
                if res.endswith("\n"):
                    res = res[:-1]
    
    # fallback
    else: 
        res = token

    # return
    if inline:
        return res
    else:
        ind = " " * depth * 4
        return f"{ind}{res}\n"

def prettifyf(filepath):
    bpath, ext = os.path.splitext(filepath)
    ppath = f"{bpath}.pre{ext}"
    with open(filepath, 'r', encoding='utf-8') as f:
        ocode = f.read()  
    tokens = tokenize(ocode)
    stream = TokenStream(tokens)
    pcode = ""
    while stream.can_push():
        chunk = prettify(stream, 0, inline=False)
        if chunk.strip():
            if chunk.startswith("{"):
                pcode += chunk + "\n"
            else:
                pcode += chunk     
    with open(ppath, 'w', encoding='utf-8') as f:
        f.write(pcode)
    print(f"Otia updated: {os.path.basename(filepath)} -> Beautiful structural layout saved to {os.path.basename(ppath)}")
    return ppath