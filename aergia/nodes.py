import operator as oper

# aergia nodes
# by las-r

# constants
UNOPS = {
    "_": oper.neg, "~": oper.inv,
    "!": lambda a: int(a == 0)
}
BINOPS = {
    "+": oper.add, "-": oper.sub, "*": oper.mul, "/": oper.truediv, "^": pow,
    "%": oper.mod, "&": oper.and_, "|": oper.or_, "$": oper.xor,
    "==": lambda a, b: int(a == b),
    "!=": lambda a, b: int(a != b),
    ">>": lambda a, b: int(a > b),
    "<<": lambda a, b: int(a < b),
    ">=": lambda a, b: int(a >= b),
    "<=": lambda a, b: int(a <= b),
}

# literal class
class LiteralNode:
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self.value

# variable nodes
class AssignNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def eval(self, env):
        value = self.value.eval(env)
        env[self.name] = value
        return value

class IdentifierNode:
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return env[self.name]

# operation nodes
class UnOpNode:
    def __init__(self, op, a):
        self.op = op
        self.a = a

    def eval(self, env):
        if self.op in UNOPS:
            a = self.a.eval(env)
            return UNOPS[self.op](a)

class BinOpNode:
    def __init__(self, op, a, b):
        self.op = op
        self.a = a
        self.b = b

    def eval(self, env):
        a = self.a.eval(env)
        if self.op == "&&" and a == 0:
            return 0
        if self.op == "||" and a != 0:
            return 1
        if self.op in BINOPS:
            b = self.b.eval(env)
            return BINOPS[self.op](a, b)