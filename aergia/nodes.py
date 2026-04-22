# aergia nodes
# made by las-r on github

# exceptions
class ReturnException(Exception):
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
        return env.get(self.name, 0)

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
            if not v: return 1
            else: return 0
        elif self.op == "~": return ~v

class BinaryOpNode:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        
    def eval(self, env):
        vl = self.left.eval(env)
        vr = self.right.eval(env)
        if self.op == "+": return vl + vr
        elif self.op == "-": return vl - vr
        elif self.op == "*": return vl * vr
        elif self.op == "/": return vl / vr
        elif self.op == "^": return vl ** vr
        elif self.op == "%": return vl % vr
        elif self.op == "|": return vl | vr
        elif self.op == "&": return vl & vr
        elif self.op == "$": return vl ^ vr
        elif self.op == "==": 
            if vl == vr: return 1
            else: return 0
        elif self.op == "!=": 
            if vl != vr: return 1
            else: return 0
        elif self.op == "<<":
            if vl < vr: return 1
            else: return 0
        elif self.op == ">>":
            if vl > vr: return 1
            else: return 0
        elif self.op == "<=":
            if vl <= vr: return 1
            else: return 0
        elif self.op == ">=":
            if vl >= vr: return 1
            else: return 0

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
        fenv = env.copy() 
        for name, argnode in zip(func.para, self.args):
            fenv[name] = argnode.eval(env)
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