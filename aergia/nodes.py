import dataclasses
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

# exceptions
@dataclasses.dataclass
class Return(Exception):
    value: Node

# function
@dataclasses.dataclass
class Function:
    params: list
    body: list

# node base
class Node: pass

# literal
class LiteralNode(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self.value

# variable
class AssignNode(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def eval(self, env):
        value = self.value.eval(env)
        env[self.name] = value
        return value

class IdentifierNode(Node):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return env[self.name]

# io
class PrintNode(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        value = self.value.eval(env)
        print(value)
        return value

class InputNode(Node):
    def __init__(self, itype):
        self.itype = itype

    def eval(self, env):
        return self.itype(input())

# math
class UnOpNode(Node):
    def __init__(self, op, a):
        self.op = op
        self.a = a

    def eval(self, env):
        if self.op in UNOPS:
            a = self.a.eval(env)
            return UNOPS[self.op](a)

class BinOpNode(Node):
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

# array
class ArrayNode(Node):
    def __init__(self, items):
        self.items = items

    def eval(self, env):
        return [i.eval(env) for i in self.items]

class IndexNode(Node):
    def __init__(self, array, index):
        self.array = array
        self.index = index

    def eval(self, env):
        return self.array.eval(env)[self.index.eval(env)] 

# control flow
class IfNode(Node):
    def __init__(self, cond, body, ebody):
        self.cond = cond
        self.body = body
        self.ebody = ebody

    def eval(self, env):
        res = 0
        if self.cond.eval(env):
            for n in self.body:
                res = n.eval(env)
        else:
            for n in self.ebody:
                res = n.eval(env)
        return res

class WhileNode(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def eval(self, env):
        res = 0
        while self.cond.eval(env):
            for n in self.body:
                res = n.eval(env)
        return res

# functional
class DefinitionNode(Node):
    def __init__(self, params, body):
        self.params = params
        self.body = body

    def eval(self, env):
        return Function(self.params, self.body)

class CallNode(Node):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def eval(self, env):
        func = self.func.eval(env)
        args = [a.eval(env) for a in self.args]
        lenv = env.copy()
        lenv[";"] = func
        for param, arg in zip(func.params, args):
            lenv[param] = arg
        res = 0
        try:
            for n in func.body:
                res = n.eval(lenv)
        except Return as r:
            res = r.value
        return res

class ReturnNode(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        raise Return(self.value.eval(env))