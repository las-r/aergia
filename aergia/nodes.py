import importlib
import json
import operator
import random
import re
from pathlib import Path

# aergia nodes
# made by las-r on github

# constants
OPS = {
    "+": lambda l, r: str(l) + str(r) if isinstance(l, str) or isinstance(r, str) else l + r,
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
class AergiaRuntimeError(Exception):
    def __init__(self, message, line, col):
        self.message = message
        self.line = line
        self.col = col
        super().__init__(self.message)
        
class BreakException(Exception): pass

class ContinueException(Exception): pass

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class ExitException(Exception):
    def __init__(self, value):
        self.value = value
        
# types
class Super:
    def __init__(self, name, consn):
        self.name = name
        self.consn = consn
        self.value = None

    def collapse(self, env):
        def find_literals(node):
            nums = []
            if not node:
                return nums
            if isinstance(node, LiteralNode) and isinstance(node.value, (int, float)):
                nums.append(node.value)
            for attr in ["left", "right", "child", "elements", "mainbody", "elsebody", "cond"]:
                if hasattr(node, attr):
                    val = getattr(node, attr)
                    if isinstance(val, list):
                        for item in val:
                            nums.extend(find_literals(item))
                    else:
                        nums.extend(find_literals(val))
            return nums
        foundnum = find_literals(self.consn)
        if foundnum:
            lowb = int(min(foundnum)) - 5
            highb = int(max(foundnum)) + 5
        else:
            lowb, highb = -100, 100
        if (highb - lowb) > 2**16:
            raise AergiaRuntimeError(
                f"Constraints are too loose for '{self.name}' (explicit range exceeds 2^16)",
                line=self.consn.line, col=self.consn.col
            )
        testenv = env.copy()
        probe_offset = 2**16 + 1
        testenv[self.name] = lowb - probe_offset
        if self.consn.eval(testenv) != 0:
            raise AergiaRuntimeError(
                f"Constraints are too loose for '{self.name}' (unbounded negative space detected)",
                line=self.consn.line, col=self.consn.col
            )
        testenv[self.name] = highb + probe_offset
        if self.consn.eval(testenv) != 0:
            raise AergiaRuntimeError(
                f"Constraints are too loose for '{self.name}' (unbounded positive space detected)",
                line=self.consn.line, col=self.consn.col
            )
        valid = []
        for candidate in range(lowb, highb + 1):
            testenv[self.name] = candidate
            if self.consn.eval(testenv) != 0:
                valid.append(candidate)
        if not valid:
            for _ in range(200):
                candidate = random.uniform(lowb, highb)
                testenv[self.name] = candidate
                if self.consn.eval(testenv) != 0:
                    valid.append(candidate)
        if not valid:
            raise AergiaRuntimeError(
                f"Constraints are too tight. No possible value found matching constraints for '{self.name}'",
                line=self.consn.line, col=self.consn.col
            )
        self.value = random.choice(valid)
        env[self.name] = self.value

    def __repr__(self):
        return f"<Supervalue '{self.name}' (uncollapsed constraints)>"

# value nodes
class LiteralNode:
    def __init__(self, value):
        self.value = value
        self.line = None
        self.col = None

    def eval(self, env):
        if not isinstance(self.value, str):
            return self.value
        try:
            from .lexer import tokenize
            from .parser import parse
            pattern = r'%(.*?)%'
            def replacer(match):
                exprcode = match.group(1).strip()
                innertokens = tokenize(exprcode)
                ast = parse(innertokens)
                res = 0
                for node in ast:
                    if node:
                        if hasattr(node, "line"):
                            node.line = self.line
                        if hasattr(node, "col"):
                            node.col = self.col
                        res = node.eval(env)
                return str(res)
            return re.sub(pattern, replacer, self.value)
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(f"Interpolation Error: {e}", line=self.line, col=self.col)

class VariableNode:
    def __init__(self, name):
        self.name = name
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            if self.name not in env:
                raise NameError(f"No variable '{self.name}' found")
            val = env[self.name]
            if isinstance(val, Super):
                val.collapse(env)
            return env[self.name]
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

# assignment node
class AssignNode:
    def __init__(self, name, child):
        self.name = name
        self.child = child
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            value = self.child.eval(env)
            env[self.name] = value
            return value
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

# super node  
class SuperNode:
    def __init__(self, name, constraints):
        self.name = name
        self.constraints = constraints
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            sv = Super(self.name, self.constraints)
            env[self.name] = sv
            return 0
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

# i/o nodes
class OutputNode:
    def __init__(self, child):
        self.child = child
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            print(self.child.eval(env))
            return 0
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class StringInputNode:
    def __init__(self):
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            return input()
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class IntInputNode:
    def __init__(self):
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            return int(input())
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class FloatInputNode:
    def __init__(self):
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            return float(input())
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

# operation nodes
class UnaryOpNode:
    def __init__(self, op, child):
        self.op = op
        self.child = child
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            v = self.child.eval(env)
            if self.op == "!":
                if not v:
                    return 1
                else:
                    return 0
            elif self.op == "~":
                return ~v
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class BinaryOpNode:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            vl = self.left.eval(env)
            vr = self.right.eval(env)
            return OPS[self.op](vl, vr)
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class ShortCircuitANDNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            if not self.left.eval(env):
                return 0
            return 1 if self.right.eval(env) else 0
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)
    
class ShortCircuitORNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            if self.left.eval(env):
                return 1
            return 1 if self.right.eval(env) else 0
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

# array nodes
class ArrayNode:
    def __init__(self, elements):
        self.elements = elements
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            return [e.eval(env) for e in self.elements]
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class IndexNode:
    def __init__(self, arrayn, indexn):
        self.arrayn = arrayn
        self.indexn = indexn
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            arr = self.arrayn.eval(env)
            idx = self.indexn.eval(env)
            if not isinstance(arr, (list, str)):
                raise TypeError(f"Object of type {type(arr).__name__} is not indexable")
            if not isinstance(idx, int):
                raise TypeError(f"Object of type {type(idx).__name__} is not an integer")
            return arr[int(idx)]
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class PushNode:
    def __init__(self, arrayn, itemn):
        self.arrayn = arrayn
        self.itemn = itemn
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            arr = self.arrayn.eval(env)
            itm = self.itemn.eval(env)
            if not isinstance(arr, list):
                raise TypeError(f"Object of type {type(arr).__name__} is not a list")
            arr.append(itm)
            return itm
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class PopNode:
    def __init__(self, arrayn):
        self.arrayn = arrayn
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            arr = self.arrayn.eval(env)
            if not isinstance(arr, list):
                raise TypeError(f"Object of type {type(arr).__name__} is not a list")
            return arr.pop()
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class PopIndexNode:
    def __init__(self, arrayn, indexn):
        self.arrayn = arrayn
        self.indexn = indexn
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            arr = self.arrayn.eval(env)
            idx = self.indexn.eval(env)
            if not isinstance(arr, list):
                raise TypeError(f"Object of type {type(arr).__name__} is not a list")
            if not isinstance(idx, int):
                raise TypeError(f"Object of type {type(idx).__name__} is not an integer")
            if idx < -len(arr) or idx >= len(arr):
                raise IndexError(f"Array index {idx} out of range (length {len(arr)})")
            return arr.pop(idx)
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class InsertNode:
    def __init__(self, arrayn, itemn, indexn):
        self.arrayn = arrayn
        self.itemn = itemn
        self.indexn = indexn
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            arr = self.arrayn.eval(env)
            itm = self.itemn.eval(env)
            idx = self.indexn.eval(env)
            if not isinstance(arr, list):
                raise TypeError(f"Object of type {type(arr).__name__} is not a list")
            if not isinstance(idx, int):
                raise TypeError(f"Object of type {type(idx).__name__} is not an integer")
            arr.insert(idx, itm)
            return itm
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class RemoveItemNode:
    def __init__(self, arrayn, itemn):
        self.arrayn = arrayn
        self.itemn = itemn
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            arr = self.arrayn.eval(env)
            itm = self.itemn.eval(env)
            if not isinstance(arr, list):
                raise TypeError(f"Object of type {type(arr).__name__} is not a list")
            if itm not in arr:
                raise ValueError(f"Item '{itm}' not found in the array")
            arr.remove(itm)
            return itm
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class SliceNode:
    def __init__(self, arrayn, startn, endn):
        self.arrayn = arrayn
        self.startn = startn
        self.endn = endn
        self.line = None
        self.col = None
    
    def eval(self, env):
        try:
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
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)
        
class SetIndexNode:
    def __init__(self, arrayn, indexn, valuen):
        self.arrayn = arrayn
        self.indexn = indexn
        self.valuen = valuen
        self.line = None
        self.col = None
        
    def eval(self, env):
        try:
            arr = self.arrayn.eval(env)
            ind = self.indexn.eval(env)
            val = self.valuen.eval(env)
            if not isinstance(arr, (list)):
                raise TypeError(f"Object of type {type(arr).__name__} is not a list")
            if not isinstance(ind, int):
                raise TypeError(f"Object of type {type(ind).__name__} is not an integer")
            arr[ind] = val
            return val
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)
        
# range node
class RangeNode:
    def __init__(self, startn, endn, incn):
        self.startn = startn
        self.endn = endn
        self.incn = incn
        self.line = None
        self.col = None
        
    def eval(self, env):
        start = self.startn.eval(env)
        end = self.endn.eval(env)
        inc = self.incn.eval(env)
        if not isinstance(start, int):
            raise TypeError(f"Object of type {type(start).__name__} is not an integer")
        if not isinstance(end, int):
            raise TypeError(f"Object of type {type(end).__name__} is not an integer")
        if not isinstance(inc, int):
            raise TypeError(f"Object of type {type(inc).__name__} is not an integer")
        return list(range(start, end, inc))

# control flow nodes
class IfNode:
    def __init__(self, cond, mainbody, elsebody=[]):
        self.cond = cond
        self.mainbody = mainbody
        self.elsebody = elsebody
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            last = 0
            if self.cond.eval(env):
                for node in self.mainbody:
                    last = node.eval(env)
            else:
                for node in self.elsebody:
                    last = node.eval(env)
            return last
        except (AergiaRuntimeError, ReturnException, ExitException, BreakException, ContinueException):
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class WhileNode:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            last = 0
            while self.cond.eval(env):
                try:
                    for node in self.body:
                            last = node.eval(env)
                except BreakException:
                    break
                except ContinueException:
                    continue
            return last
        except (AergiaRuntimeError, ReturnException, ExitException):
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class ForNode:
    def __init__(self, array, iname, body):
        self.array = array
        self.iname = iname
        self.body = body
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            iterable = self.array.eval(env)
            if not hasattr(iterable, "__iter__"):
                raise TypeError(f"'{type(iterable).__name__}' object is not iterable")
            last = 0
            for item in iterable:
                env[self.iname] = item
                try:
                    for node in self.body:
                        last = node.eval(env)
                except BreakException:
                    break
                except ContinueException:
                    continue
            return last
        except (AergiaRuntimeError, ReturnException, ExitException):
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)
        
class BreakNode:
    def __init__(self):
        self.line = None
        self.col = None
    
    def eval(self, env):
        raise BreakException()
        
    
class ContinueNode:
    def __init__(self):
        self.line = None
        self.col = None 
        
    def eval(self, env):
        raise ContinueException()

# function nodes
class FunctionNode:
    def __init__(self, name, para, body):
        self.name = name
        self.para = para
        self.body = body
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            self.capturedenv = env.copy()
            env[self.name] = self
            return 0
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)
        
class AnonymousFunctionNode:
    def __init__(self, para, ret):
        self.para = para
        self.ret = ret
        self.line = None
        self.col = None
        
    def eval(self, env):
        try:
            self.capturedenv = env.copy()
            return self
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class CallNode:
    def __init__(self, target, args):
        self.target = target
        self.args = args
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            func = self.target.eval(env)
            if not func:
                raise Exception("Target is not a valid function")
            eargs = [arg.eval(env) for arg in self.args]
            if callable(func):
                return func(*eargs)
            fenv = func.capturedenv.copy() if hasattr(func, "capturedenv") else env.copy()
            for name, val in zip(func.para, eargs):
                fenv[name] = val
            body = func.body if hasattr(func, "body") else func.ret
            if not isinstance(body, list):
                body = [body]
            try:
                last = 0
                for node in body:
                    last = node.eval(fenv)
                return last
            except ReturnException as e:
                return e.value
        except (AergiaRuntimeError, ExitException):
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class ReturnNode:
    def __init__(self, value):
        self.value = value
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            raise ReturnException(self.value.eval(env))
        except (AergiaRuntimeError, ReturnException):
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

# import nodes
class ImportNode:
    def __init__(self, file):
        self.file = file
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            from .lexer import tokenize
            from .parser import parse
            import json
            filename = self.file.eval(env)
            file = env["__dir__"] / filename
            if not file.exists() and "__stdlib__" in env:
                fbfile = env["__stdlib__"] / filename
                if fbfile.exists():
                    file = fbfile
            if not file.exists() and "__lib__" in env:
                libdir = env["__lib__"]
                pkgdir = libdir / filename
                if pkgdir.is_dir():
                    manifestpath = pkgdir / "aerpkg.json"
                    srcfolder = ""
                    if manifestpath.exists():
                        try:
                            with open(manifestpath, "r") as f:
                                data = json.load(f)
                                srcfolder = data.get("src", "")
                        except (json.JSONDecodeError, KeyError):
                            pass
                    candidate = pkgdir / srcfolder / "main.aer"
                    if candidate.exists():
                        file = candidate
            if not file.exists():
                raise AergiaRuntimeError(f"Could not resolve import: '{filename}'", line=self.line, col=self.col)
            file = file.resolve()
            if "__imports__" not in env:
                env["__imports__"] = set()
            if file in env["__imports__"]:
                return 0
            env["__imports__"].add(file)
            with open(file, "r") as f:
                code = f.read()
            tokens = tokenize(code)
            ast = parse(tokens)
            olddir = env.get("__dir__")
            env["__dir__"] = file.parent
            last = 0
            for node in ast:
                if node:
                    last = node.eval(env)
            if olddir is not None:
                env["__dir__"] = olddir
            return last
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class PyImportNode:
    def __init__(self, name, rname, closed):
        self.name = name
        self.rname = rname
        self.closed = closed
        self.line = None
        self.col = None

    def eval(self, env):
        try:
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
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

# system nodes
class EvaluationNode:
    def __init__(self, value):
        self.value = value
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            from .lexer import tokenize
            from .parser import parse
            code = self.value.eval(env)
            tokens = tokenize(code)
            ast = parse(tokens)
            last = 0
            for node in ast:
                if node:
                    last = node.eval(env)
            return last
        except (AergiaRuntimeError, ReturnException, ExitException):
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)

class ExitNode:
    def __init__(self, value):
        self.value = value
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            exitc = self.value.eval(env)
            raise ExitException(exitc)
        except (AergiaRuntimeError, ExitException):
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col)