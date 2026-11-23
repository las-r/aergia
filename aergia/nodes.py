from __future__ import annotations
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
    "&&": None, "||": "None"
}

# helper functions
def check(val, types):
    if isinstance(val, types):
        return val
    raise TypeError(f"Expected '{val}' to be in {types}, got {type(val)} instead")

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
    def __init__(self, msg):
        self.msg = msg

    def eval(self, env):
        return input(self.msg.eval(env))

# type conversion
class ConvertNode(Node):
    def __init__(self, value, typec):
        self.value = value
        self.typec = typec

    def eval(self, env):
        return self.typec(self.value.eval(env))

# math
class UnOpNode(Node):
    def __init__(self, op, a):
        self.op = op
        self.a = a

    def eval(self, env):
        if self.op in UNOPS:
            a = check(self.a.eval(env), (int, float))
            return UNOPS[self.op](a)

class BinOpNode(Node):
    def __init__(self, op, a, b):
        self.op = op
        self.a = a
        self.b = b

    def eval(self, env):
        a = check(self.a.eval(env), (int, float, str))
        if self.op == "&&" and a == 0:
            return 0
        if self.op == "||" and a != 0:
            return 1
        if self.op in BINOPS:
            b = check(self.b.eval(env), (int, float, str))
            return BINOPS[self.op](a, b)

# map
class MapNode(Node):
    def eval(self, env):
        return {}

class SizeNode(Node):
    def __init__(self, map_):
        self.map_ = map_

    def eval(self, env):
        return len(check(self.map_.eval(env), dict))

class GetNode(Node):
    def __init__(self, map_, key):
        self.map_ = map_
        self.key = key

    def eval(self, env):
        return check(self.map_.eval(env), dict).get(self.key.eval(env), 0)

class SetNode(Node):
    def __init__(self, name, key, value):
        self.name = name
        self.key = key
        self.value = value

    def eval(self, env):
        value = check(self.value.eval(env), dict)
        env[self.name][self.key.eval(env)] = value
        return value

# control flow
class IfNode(Node):
    def __init__(self, cond, body, ebody):
        self.cond = cond
        self.body = body
        self.ebody = ebody

    def eval(self, env):
        res = 0
        if self.cond.eval(env) != 0:
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
        while self.cond.eval(env) != 0:
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
        func = check(self.func.eval(env), Function)
        args = [a.eval(env) for a in self.args]
        lenv = env | {";": func} | {p: a for p, a in zip(func.params, args)}
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