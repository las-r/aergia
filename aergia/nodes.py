import importlib
import json
import operator
import random
import re
from collections.abc import MutableMapping
from typing import Any, Iterator

# aergia nodes
# made by las-r on github

# constants
BINOPS = {
    "+": operator.add,
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
    "&&": None,
    "||": None,
}
UNOPS = {
    "~": operator.inv,
    "!": operator.not_,
    "=,": str,
    "=.": int,
    "='": float,
}
ETYPEMAP = {
    "ZeroDivisionError": "DivisionByZero",
    "IndexError": "IndexOutOfRange",
    "KeyError": "KeyNotFound",
    "TypeError": "TypeError",
    "NameError": "NameError",
    "ValueError": "ValueError",
    "FileNotFoundError": "FileNotFound",
    "PermissionError": "PermissionDenied",
}

# exceptions
class AergiaRuntimeError(Exception):
    def __init__(self, message, line, col, etype="RuntimeError"):
        self.message = message
        self.line = line
        self.col = col
        self.etype = etype
        self.frames = []
        super().__init__(self.message)
        
class BreakException(Exception): 
    pass

class ContinueException(Exception): 
    pass

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class ExitException(Exception):
    def __init__(self, value):
        self.value = value
        
# environment
class Environment(MutableMapping):
    def __init__(self, bindings=None, parent=None):
        self.bindings = bindings if bindings is not None else {}
        self.parent = parent

    def __getitem__(self, key: str) -> Any:
        if key in self.bindings:
            return self.bindings[key]
        if self.parent is not None:
            return self.parent[key]
        raise KeyError(f"No variable '{key}' found")

    def __setitem__(self, key: str, value: Any) -> None:
        if key in self.bindings:
            self.bindings[key] = value
        elif self.parent is not None and key in self.parent:
            self.parent[key] = value
        else:
            self.bindings[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.bindings:
            del self.bindings[key]
        elif self.parent is not None:
            del self.parent[key]
        else:
            raise KeyError(f"No variable '{key}' found")

    def __contains__(self, key: object) -> bool:
        if key in self.bindings:
            return True
        if self.parent is not None:
            return key in self.parent
        return False

    def __iter__(self) -> Iterator[str]:
        seen = set(self.bindings.keys())
        for k in self.bindings:
            yield k
        if self.parent is not None:
            for k in self.parent:
                if k not in seen:
                    yield k

    def __len__(self) -> int:
        return len(list(self.__iter__()))

    def get(self, key: str, default: Any = None) -> Any:
        if key in self.bindings:
            return self.bindings[key]
        if self.parent is not None:
            return self.parent.get(key, default)
        return default

    def copy(self):
        return Environment(parent=self)
        
# object helpers
class CustomClass:
    def __init__(self, name, para, body, defenv):
        self.name = name
        self.para = para
        self.body = body
        self.defenv = defenv

    def __call__(self, *eargs):
        instance = CustomInstance(self)
        instance_env = Environment(parent=self.defenv)
        instance.env = instance_env
        instance_env["this"] = instance
        for param, arg in zip(self.para, eargs):
            instance_env.bindings[param] = arg
        for node in self.body:
            if node:
                node.eval(instance_env)
        return instance

    def __repr__(self):
        return f"<class {self.name}>"

class CustomInstance:
    def __init__(self, customclass):
        self.customclass = customclass
        self.env = Environment()

    def __repr__(self):
        return f"<instance of class {self.customclass.name}>"

class BoundMethod:
    def __init__(self, instance, funcn):
        self.instance = instance
        self.funcn = funcn

    def __call__(self, *args):
        fullargs = [self.instance] + list(args)
        fenv = Environment(parent=self.instance.env)
        if hasattr(self.funcn, "para"):
            for param, arg in zip(self.funcn.para, fullargs):
                fenv.bindings[param] = arg
        body = self.funcn.body if hasattr(self.funcn, "body") else self.funcn.ret
        if not isinstance(body, list):
            body = [body]
        try:
            last = 0
            for node in body:
                if node:
                    last = node.eval(fenv)
            return last
        except ReturnException as e:
            return e.value

# types
class Super:
    def __init__(self, name, consn):
        self.name = name
        self.consn = consn
        self.value = None

    def collapse(self, env):
        def findliterals(node):
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
                            nums.extend(findliterals(item))
                    else:
                        nums.extend(findliterals(val))
            return nums
        foundnum = findliterals(self.consn)
        if foundnum:
            lowb = int(min(foundnum)) - 5
            highb = int(max(foundnum)) + 5
        else:
            lowb = -100
            highb = 100
        if (highb - lowb) > 2**16:
            raise AergiaRuntimeError(
                f"Constraints are too loose for '{self.name}' (explicit range exceeds 2^16)",
                line=self.consn.line, col=self.consn.col, etype="ConstraintError"
            )
        testenv = env.copy()
        probe_offset = 2**16 + 1
        testenv[self.name] = lowb - probe_offset
        if self.consn.eval(testenv) != 0:
            raise AergiaRuntimeError(
                f"Constraints are too loose for '{self.name}' (unbounded negative space detected)",
                line=self.consn.line, col=self.consn.col, etype="ConstraintError"
            )
        testenv[self.name] = highb + probe_offset
        if self.consn.eval(testenv) != 0:
            raise AergiaRuntimeError(
                f"Constraints are too loose for '{self.name}' (unbounded positive space detected)",
                line=self.consn.line, col=self.consn.col, etype="ConstraintError"
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
                line=self.consn.line, col=self.consn.col, etype="ConstraintError"
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
            raise AergiaRuntimeError(f"Interpolation Error: {e}", line=self.line, col=self.col, etype="InterpolationError")

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
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

# assignment nodes
class AssignNode:
    def __init__(self, name, child, scoped=False):
        self.name = name
        self.child = child
        self.scoped = scoped
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            value = self.child.eval(env)
            if self.scoped:
                env.bindings[self.name] = value
            else:
                env[self.name] = value
            return value
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

class SuperAssignNode:
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
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

# i/o nodes
class OutputNode:
    def __init__(self, child):
        self.child = child
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            val = self.child.eval(env)
            print(val)
            return val
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

class StringInputNode:
    def __init__(self):
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            return input()
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

class IntInputNode:
    def __init__(self):
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            return int(input())
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

class FloatInputNode:
    def __init__(self):
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            return float(input())
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

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
            if self.op in UNOPS:
                return UNOPS[self.op](v)
            else:
                raise SyntaxError(f"'{self.op}' is not a valid operator.")
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

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
            if self.op in BINOPS:
                return BINOPS[self.op](vl, vr)
            else:
                raise SyntaxError(f"'{self.op}' is not a valid operator.")
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

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
            if self.right.eval(env):
                return 1
            else:
                return 0
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))
    
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
            if self.right.eval(env):
                return 1
            else:
                return 0
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

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
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

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
            if isinstance(arr, dict):
                return arr[idx]
            if not isinstance(arr, (list, str)):
                raise TypeError(f"Object of type {type(arr).__name__} is not indexable")
            return arr[int(idx)]
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

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
            if isinstance(arr, dict):
                if isinstance(itm, dict):
                    arr.update(itm)
                elif isinstance(itm, (list, tuple)) and len(itm) == 2:
                    arr[itm[0]] = itm[1]
                else:
                    raise TypeError("To push to a dictionary, the item must be another dictionary or a [key, value] pair")
                return itm
            if not isinstance(arr, list):
                raise TypeError(f"Object of type {type(arr).__name__} is not a list or dictionary")
            arr.append(itm)
            return itm
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

class PopNode:
    def __init__(self, arrayn):
        self.arrayn = arrayn
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            arr = self.arrayn.eval(env)
            if isinstance(arr, dict):
                if not arr:
                    raise KeyError("popitem(): dictionary is empty")
                return list(arr.popitem())
            if not isinstance(arr, list):
                raise TypeError(f"Object of type {type(arr).__name__} is not a list or dictionary")
            return arr.pop()
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

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
            if isinstance(arr, dict):
                if idx not in arr:
                    raise KeyError(f"Key '{idx}' not found in the dictionary")
                return arr.pop(idx)
            if not isinstance(arr, list):
                raise TypeError(f"Object of type {type(arr).__name__} is not a list or dictionary")
            if not isinstance(idx, int):
                raise TypeError(f"Object of type {type(idx).__name__} is not an integer")
            if idx < -len(arr) or idx >= len(arr):
                raise IndexError(f"Array index {idx} out of range (length {len(arr)})")
            return arr.pop(idx)
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

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
            if isinstance(arr, dict):
                arr[idx] = itm
                return itm
            if not isinstance(arr, list):
                raise TypeError(f"Object of type {type(arr).__name__} is not a list or dictionary")
            if not isinstance(idx, int):
                raise TypeError(f"Object of type {type(idx).__name__} is not an integer")
            arr.insert(idx, itm)
            return itm
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

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
            if isinstance(arr, dict):
                if itm not in arr:
                    raise KeyError(f"Key '{itm}' not found in the dictionary")
                del arr[itm]
                return itm
            if not isinstance(arr, list):
                raise TypeError(f"Object of type {type(arr).__name__} is not a list or dictionary")
            if itm not in arr:
                raise ValueError(f"Item '{itm}' not found in the array")
            arr.remove(itm)
            return itm
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

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
                raise TypeError(f"Object of type {type(arr).__name__} is not sliceable")
            if not isinstance(start, int):
                raise TypeError(f"Object of type {type(start).__name__} is not an integer")
            if not isinstance(end, int):
                raise TypeError(f"Object of type {type(end).__name__} is not an integer")
            return arr[start:end]
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))
        
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
            if isinstance(arr, dict):
                arr[ind] = val
                return val
            if not isinstance(arr, list):
                raise TypeError(f"Object of type {type(arr).__name__} is not a list or dictionary")
            if not isinstance(ind, int):
                raise TypeError(f"Object of type {type(ind).__name__} is not an integer")
            arr[ind] = val
            return val
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

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
    
# map node
class MapNode:
    def __init__(self, pairs):
        self.pairs = pairs
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            return {k.eval(env): v.eval(env) for k, v in self.pairs}
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))
        
# file nodes
class OpenFileNode:
    def __init__(self, filenamen, actn):
        self.filenamen = filenamen
        self.actn = actn
        self.line = None
        self.col = None
    
    def eval(self, env):
        try:
            filename = self.filenamen.eval(env)
            act = self.actn.eval(env)
            return open(filename, act)
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))
        
class ReadFileNode:
    def __init__(self, filen):
        self.filen = filen
        self.line = None
        self.col = None
    
    def eval(self, env):
        try:
            file = self.filen.eval(env)
            return file.read()
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

class WriteFileNode:
    def __init__(self, filen, valn):
        self.filen = filen
        self.valn = valn
        self.line = None
        self.col = None
    
    def eval(self, env):
        try:
            file = self.filen.eval(env)
            val = self.valn.eval(env)
            file.write(val)
            return val
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))
        
class CloseFileNode:
    def __init__(self, filen):
        self.filen = filen
        self.line = None
        self.col = None
    
    def eval(self, env):
        try:
            file = self.filen.eval(env)
            file.close()
            return 0
        except AergiaRuntimeError:
            raise
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

# control flow nodes
class IfNode:
    def __init__(self, cond, mainbody, elsebody=None):
        self.cond = cond
        self.mainbody = mainbody
        self.elsebody = elsebody if elsebody is not None else []
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
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

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
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

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
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))
        
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
    
# error catching node
class TryCatchNode:
    def __init__(self, errname, body, catchbody):
        self.errname = errname
        self.body = body
        self.catchbody = catchbody
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            last = 0
            for node in self.body:
                if node:
                    last = node.eval(env)
            return last
        except AergiaRuntimeError as e:
            catchenv = env.copy()
            catchenv[self.errname] = e.message
            catchenv[self.errname + ".type"] = e.etype
            last = 0
            for node in self.catchbody:
                if node:
                    last = node.eval(catchenv)
            return last
        except ExitException:
            raise

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
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))
        
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
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))
        
class UnpackNode:
    def __init__(self, node):
        self.node = node
        self.line = None
        self.col = None
    
    def eval(self, env):
        return self.node.eval(env)

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
                raise AergiaRuntimeError("Target is not a valid function", line=self.line, col=self.col, etype="TypeError")
            eargs = []
            for arg in self.args:
                val = arg.eval(env)
                if isinstance(arg, UnpackNode):
                    eargs.extend(val)
                else:
                    eargs.append(val)
            if callable(func):
                return func(*eargs)
            if hasattr(func, "capturedenv"):
                fenv = func.capturedenv.copy()
            else:
                fenv = env.copy()
            if hasattr(func, "para"):
                if len(func.para) != len(eargs):
                    raise AergiaRuntimeError(f"Function takes {len(func.para)} arguments, but {len(eargs)} were given", line=self.line, col=self.col, etype="TypeError")
                for param, arg in zip(func.para, eargs, strict=True):
                    fenv.bindings[param] = arg
            if hasattr(func, "body"):
                body = func.body
            else:
                body = func.ret
            if not isinstance(body, list):
                body = [body]
            try:
                last = 0
                for node in body:
                    if node:
                        last = node.eval(fenv)
                return last
            except ReturnException as e:
                return e.value
            except AergiaRuntimeError as e:
                if not e.frames:
                    e.frames.append((fenv.get("__file__"), e.line, e.col))
                raise e
        except AergiaRuntimeError as e:
            if not e.frames:
                e.frames.append((env.get("__file__"), e.line, e.col))
            else:
                e.frames.append((env.get("__file__"), self.line, self.col))
            raise e
        except ExitException:
            raise
        except Exception as e:
            err = AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))
            err.frames = [(env.get("__file__"), self.line, self.col)]
            raise err

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
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

# object nodes
class ClassNode:
    def __init__(self, name, para, body):
        self.name = name
        self.para = para
        self.body = body
        self.line = None
        self.col = None

    def eval(self, env):
        class_ = CustomClass(self.name, self.para, self.body, env)
        env[self.name] = class_
        return 0

class GetMemberNode:
    def __init__(self, objn, propname):
        self.objn = objn
        self.propname = propname
        self.line = None
        self.col = None

    def eval(self, env):
        obj = self.objn.eval(env)
        if isinstance(obj, CustomInstance):
            val = obj.env.get(self.propname)
            if isinstance(val, (FunctionNode, AnonymousFunctionNode)):
                return BoundMethod(obj, val)
            return val
        if isinstance(obj, dict):
            return obj[self.propname]
        return getattr(obj, self.propname)

class SetMemberNode:
    def __init__(self, objn, propname, valn):
        self.objn = objn
        self.propname = propname
        self.valn = valn
        self.line = None
        self.col = None

    def eval(self, env):
        obj = self.objn.eval(env)
        val = self.valn.eval(env)
        if isinstance(obj, CustomInstance):
            obj.env[self.propname] = val
            return val
        if isinstance(obj, dict):
            obj[self.propname] = val
            return val
        setattr(obj, self.propname, val)
        return val

# import nodes
class ImportNode:
    def __init__(self, file, rname, closed):
        self.file = file
        self.rname = rname
        self.closed = closed
        self.line = None
        self.col = None

    def eval(self, env):
        try:
            from .lexer import tokenize
            from .parser import parse
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
                raise AergiaRuntimeError(f"Could not resolve import: '{filename}'", line=self.line, col=self.col, etype="ImportError")
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
            menv = env.copy()
            menv["__file__"] = file
            menv["__dir__"] = file.parent
            last = 0
            try:
                for node in ast:
                    if node:
                        last = node.eval(menv)
            except AergiaRuntimeError as e:
                if not e.frames:
                    e.frames.append((file, e.line, e.col))
                raise e
            for key, val in menv.bindings.items():
                if key in ("__file__", "__dir__", "__imports__"):
                    continue
                if self.closed:
                    env[f"{self.rname}.{key}"] = val
                else:
                    env[key] = val
            return last
        except AergiaRuntimeError as e:
            if not e.frames:
                e.frames.append((env.get("__file__"), e.line, e.col))
            else:
                e.frames.append((env.get("__file__"), self.line, self.col))
            raise e
        except ExitException:
            raise
        except Exception as e:
            err = AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))
            err.frames = [(env.get("__file__"), self.line, self.col)]
            raise err

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
                        env[f"{self.rname}.{name}"] = value
                    if isinstance(value, type):
                        for sname, sval in vars(value).items():
                            if not sname.startswith("_"):
                                if not self.closed:
                                    env[f"{name}.{sname}"] = sval
                                else:
                                    env[f"{self.rname}.{name}.{sname}"] = sval
            return 0
        except Exception as e:
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))

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
            try:
                for node in ast:
                    if node:
                        last = node.eval(env)
            except AergiaRuntimeError as e:
                if not e.frames:
                    e.frames.append(("<dynamic code>", e.line, e.col))
                raise e
            return last
        except AergiaRuntimeError as e:
            if not e.frames:
                e.frames.append((env.get("__file__"), e.line, e.col))
            else:
                e.frames.append((env.get("__file__"), self.line, self.col))
            raise e
        except (ReturnException, ExitException):
            raise
        except Exception as e:
            err = AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))
            err.frames = [(env.get("__file__"), self.line, self.col)]
            raise err

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
            raise AergiaRuntimeError(str(e), line=self.line, col=self.col, etype=ETYPEMAP.get(type(e).__name__, "RuntimeError"))