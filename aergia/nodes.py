import importlib
import operator

from .lexer import tokenize

# aergia nodes
# made by las-r on github

# constants
OPS = {
    "+": lambda l, r: (
        str(l) + str(r) if isinstance(l, str) or isinstance(r, str) else l + r
    ),
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "^": operator.pow,
    "%": operator.mod,
    "|": operator.or_,
    "&": operator.and_,
    "$": operator.xor,
    "==": lambda l, r: 1 if l == r else 0,
    "!=": lambda l, r: 1 if l != r else 0,
    "<<": lambda l, r: 1 if l < r else 0,
    ">>": lambda l, r: 1 if l > r else 0,
    "<=": lambda l, r: 1 if l <= r else 0,
    ">=": lambda l, r: 1 if l >= r else 0,
}

# exceptions
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class ExitException(Exception):
    def __init__(self, value):
        self.value = value

# value nodes
class LiteralNode:
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self.value

class VariableNode:
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        if self.name not in env:
            raise NameError(f"No variable '{self.name}' found")
        return env[self.name]

# assignment
class AssignNode:
    def __init__(self, name, child):
        self.name = name
        self.child = child

    def eval(self, env):
        value = self.child.eval(env)
        env[self.name] = value
        return value

# output
class OutputNode:
    def __init__(self, child):
        self.child = child

    def eval(self, env):
        print(self.child.eval(env))
        return 0

# input
class StringInputNode:
    def __init__(self):
        pass

    def eval(self, env):
        return input()


class IntInputNode:
    def __init__(self):
        pass

    def eval(self, env):
        return int(input())

class FloatInputNode:
    def __init__(self):
        pass

    def eval(self, env):
        return float(input())

# operation nodes
class UnaryOpNode:
    def __init__(self, op, child):
        self.op = op
        self.child = child

    def eval(self, env):
        v = self.child.eval(env)
        if self.op == "!":
            if not v:
                return 1
            else:
                return 0
        elif self.op == "~":
            return ~v

class BinaryOpNode:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env):
        vl = self.left.eval(env)
        vr = self.right.eval(env)
        return OPS[self.op](vl, vr)

class ShortCircuitANDNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        if not self.left.eval(env):
            return 0
        return 1 if self.right.eval(env) else 0
    
class ShortCircuitORNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        if self.left.eval(env):
            return 1
        return 1 if self.right.eval(env) else 0

# array nodes
class ArrayNode:
    def __init__(self, elements):
        self.elements = elements

    def eval(self, env):
        return [e.eval(env) for e in self.elements]

class IndexNode:
    def __init__(self, arrayn, indexn):
        self.arrayn = arrayn
        self.indexn = indexn

    def eval(self, env):
        arr = self.arrayn.eval(env)
        idx = self.indexn.eval(env)
        if not isinstance(arr, (list, str)):
            raise TypeError(f"Object of type {type(arr).__name__} is not indexable")
        if not isinstance(idx, int):
            raise TypeError(f"Object of type {type(idx).__name__} is not an integer")
        return arr[int(idx)]

class PushNode:
    def __init__(self, arrayn, itemn):
        self.arrayn = arrayn
        self.itemn = itemn

    def eval(self, env):
        arr = self.arrayn.eval(env)
        itm = self.itemn.eval(env)
        if not isinstance(arr, list):
            raise TypeError(f"Object of type {type(arr).__name__} is not a list")
        arr.append(itm)
        return itm

class PopNode:
    def __init__(self, arrayn):
        self.arrayn = arrayn

    def eval(self, env):
        arr = self.arrayn.eval(env)
        if not isinstance(arr, list):
            raise TypeError(f"Object of type {type(arr).__name__} is not a list")
        return arr.pop()

class PopIndexNode:
    def __init__(self, arrayn, indexn):
        self.arrayn = arrayn
        self.indexn = indexn

    def eval(self, env):
        arr = self.arrayn.eval(env)
        idx = self.indexn.eval(env)
        if not isinstance(arr, list):
            raise TypeError(f"Object of type {type(arr).__name__} is not a list")
        if not isinstance(idx, int):
            raise TypeError(f"Object of type {type(idx).__name__} is not an integer")
        if idx < -len(arr) or idx >= len(arr):
            raise IndexError(f"Array index {idx} out of range (length {len(arr)})")
        return arr.pop(idx)

class InsertNode:
    def __init__(self, arrayn, itemn, indexn):
        self.arrayn = arrayn
        self.itemn = itemn
        self.indexn = indexn

    def eval(self, env):
        arr = self.arrayn.eval(env)
        itm = self.itemn.eval(env)
        idx = self.indexn.eval(env)
        if not isinstance(arr, list):
            raise TypeError(f"Object of type {type(arr).__name__} is not a list")
        if not isinstance(idx, int):
            raise TypeError(f"Object of type {type(idx).__name__} is not an integer")
        arr.insert(idx, itm)
        return itm

class RemoveItemNode:
    def __init__(self, arrayn, itemn):
        self.arrayn = arrayn
        self.itemn = itemn

    def eval(self, env):
        arr = self.arrayn.eval(env)
        itm = self.itemn.eval(env)
        if not isinstance(arr, list):
            raise TypeError(f"Object of type {type(arr).__name__} is not a list")
        if itm not in arr:
            raise ValueError(f"Item '{itm}' not found in the array")
        arr.remove(itm)
        return itm

class SliceNode:
    def __init__(self, arrayn, startn, endn):
        self.arrayn = arrayn
        self.startn = startn
        self.endn = endn
    
    def eval(self, env):
        arr = self.arrayn.eval(env)
        start = self.startn.eval(env)
        end = self.endn.eval(env)
        if not isinstance(arr, (list, str)):
            raise TypeError(f"Object of type {type(arr).__name__} is not slicable")
        if not isinstance(start, int):
            raise TypeError(f"Object of type {type(start).__name__} is not an integer")
        if not isinstance(end, int):
            raise TypeError(f"Object of type {type(end).__name__} is not an integer")
        return arr[start:end]

# control flow nodes
class IfNode:
    def __init__(self, cond, mainbody, elsebody=[]):
        self.cond = cond
        self.mainbody = mainbody
        self.elsebody = elsebody

    def eval(self, env):
        last = 0
        if self.cond.eval(env):
            for node in self.mainbody:
                last = node.eval(env)
        else:
            for node in self.elsebody:
                last = node.eval(env)
        return last

class WhileNode:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def eval(self, env):
        last = 0
        while self.cond.eval(env):
            for node in self.body:
                last = node.eval(env)
        return last

class ForNode:
    def __init__(self, array, iname, body):
        self.array = array
        self.iname = iname
        self.body = body

    def eval(self, env):
        iterable = self.array.eval(env)
        if not hasattr(iterable, "__iter__"):
            raise TypeError(f"'{type(iterable).__name__}' object is not iterable")
        last = 0
        for item in iterable:
            env[self.iname] = item
            for node in self.body:
                last = node.eval(env)
        return last

# function nodes
class FunctionNode:
    def __init__(self, name, para, body):
        self.name = name
        self.para = para
        self.body = body

    def eval(self, env):
        env[self.name] = self
        return 0

class CallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def eval(self, env):
        func = env.get(self.name)
        if not func:
            raise Exception(f"Function {self.name} not defined")
        eargs = [arg.eval(env) for arg in self.args]
        if callable(func):
            return func(*eargs)
        fenv = env.copy()
        for name, val in zip(func.para, eargs):
            fenv[name] = val
        try:
            for node in func.body:
                node.eval(fenv)
            return 0
        except ReturnException as e:
            return e.value

class ReturnNode:
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        raise ReturnException(self.value.eval(env))

# import nodes
class ImportNode:
    def __init__(self, file):
        self.file = file

    def eval(self, env):
        from .parser import parse

        file = env["__dir__"] / self.file.eval(env)
        if "__imports__" not in env:
            env["__imports__"] = set()
        if file in env["__imports__"]:
            return 0
        env["__imports__"].add(file)
        try:
            with open(file, "r") as f:
                code = f.read()
            try:
                tokens = tokenize(code)
                ast = parse(tokens)
                for node in ast:
                    if node:
                        node.eval(env)
            except Exception as e:
                print(f"Aergia Error ({file}): {e}")
        except FileNotFoundError:
            print(f"Aergia Error: Module {file} not found.")
        return 0

class PyImportNode:
    def __init__(self, name, rname, closed):
        self.name = name
        self.rname = rname
        self.closed = closed

    def eval(self, env):
        module = importlib.import_module(self.name)
        for name, value in vars(module).items():
            if not name.startswith("_"):
                if not self.closed:
                    env[name] = value
                else:
                    env[f"{self.rname}_{name}"] = value
                if isinstance(value, type):
                    for sname, sval in vars(value).items():
                        if not sname.startswith("_"):
                            if not self.closed:
                                env[f"{name}_{sname}"] = sval
                            else:
                                env[f"{self.rname}_{name}_{sname}"] = sval
        return 0

# low control nodes
class EvaluationNode:
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        from .parser import parse
        code = self.value.eval(env)
        tokens = tokenize(code)
        ast = parse(tokens)
        last = 0
        for node in ast:
            if node:
                last = node.eval(env)
        return last

class ExitNode:
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        exitc = self.value.eval(env)
        raise ExitException(exitc)