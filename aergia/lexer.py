import codecs
import re

# aergia lexer
# by las-r

# regex pattern
REGEX = re.compile(r"""
    (?P<COMMENT>  \#.*) |
    (?P<NUMBER>   \d+(?:\.\d+)?) |
    (?P<STRING>   "(?:\\.|[^"\\])*") |
    (?P<DELIM>    [()\[\]{}:]) |
    (?P<OPERATOR> ==|!=|<<|>>|<=|>=|&&|\|\||[+\-*/%^&\|$~!_]) |
    (?P<SYMBOL>   [=>.,'?]) |
    (?P<IDENT>    [a-zA-Z][a-zA-Z0-9]*) |
    (?P<SKIP>     [ \t\r\n]+) |
    (?P<MISMATCH> .)
""", re.VERBOSE)

# tokens class
class Tokens:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        
    def can_eat(self):
        return self.i < len(self.tokens)
        
    def eat(self):
        self.i += 1
        return self.tokens[self.i - 1]
    
    def peek(self):
        if self.i >= len(self.tokens):
            return ""
        return self.tokens[self.i]
    
    def expect(self, val):
        if self.peek() != val:
            raise SyntaxError(f"Expected {val}, got {self.peek()}")
        self.eat()
    
# tokenizer
def tokenize(code):
    tokens = []
    for match in REGEX.finditer(code):
        typ = match.lastgroup
        val = match.group()
        if typ == "STRING":
            val = f'"{codecs.decode(val[1:-1], "unicode_escape")}"'
        if typ in ("SKIP", "COMMENT"):
            continue
        elif typ == "MISMATCH":
            raise SyntaxError(f"Unexpected token: {val}")
        tokens.append(val)
    return Tokens(tokens)