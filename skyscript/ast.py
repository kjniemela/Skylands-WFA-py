from config import config
from vec import Vec
from world.platform import Surface, Platform

from skyscript.lexer import Token

class Event:
    def __init__(self, event, target):
        self.event = event
        self.target = target

    def __repr__(self):
        return "Event(%s @ %s)" % (self.event, self.target)

    def get_key(self):
        return "%s@%s" % (self.event, self.target.get_uuid())

def tab(indent):
    return indent * "  "

class Node:
    def __init__(self):
        pass

    def run(self, env):
        pass

    def display(self, indent=0):
        return tab(indent) + "Node()\n"

class Block(Node):
    def __init__(self, stms):
        self.stms = stms

    def run(self, env):
        for stm in self.stms:
            stm.run(env)

    def display(self, indent=0):
        rep = "Block(\n"
        for stm in self.stms:
            rep += tab(indent+1) + stm.display(indent+1)
        rep += tab(indent) + ")\n"

        return rep

class Prog(Node):
    def __init__(self, block):
        self.block = block

    def run(self, env):
        self.block.run(env)

    def display(self, indent=0):
        rep = "Prog(\n"
        rep += tab(indent+1) + self.block.display(indent+1)
        rep += tab(indent) + ")\n"

        return rep

class Stm(Node):
    def __init__(self):
        pass

    def run(self, env):
        pass

    def display(self, indent=0):
        return tab(indent) + "Stm()\n"

class LetStm(Stm):
    def __init__(self, var, exp):
        self.var = var
        self.exp = exp

    def run(self, env):
        env.scope.insert(self.var, self.exp.run(env))

    def display(self, indent=0):
        rep = "LetStm(\n"
        rep += tab(indent+1) + self.var + "\n"
        rep += tab(indent+1) + self.exp.display(indent+1) if self.exp else "None"
        rep += tab(indent) + ")\n"

        return rep

class IfStm(Stm):
    def __init__(self, exp, block):
        self.exp = exp
        self.block = block

    def run(self, env):
        if self.exp.run(env):
            return self.block.run(env)

    def display(self, indent=0):
        rep = "IfStm(\n"
        rep += tab(indent+1) + self.exp.display(indent+1)
        rep += tab(indent+1) + self.block.display(indent+1)
        rep += tab(indent) + ")\n"

        return rep

class OnStm(Stm):
    def __init__(self, event, args, block):
        self.event = event
        self.args = args
        self.block = block

    def run(self, env):
        env.add_func(self.event.run(env), self)

    def trigger(self, env, args):
        ## TODO
        event = self.event.run(env) 
        # print("ONSTM TRIGGERED", event.get_key() if type(event) == Event else event, args, self.args)
        env.scope.push_scope()
        for arg in self.args:
            env.scope.insert(arg, args[arg])
        self.block.run(env)
        env.scope.pop_scope()

    def display(self, indent=0):
        rep = "OnStm(\n"
        rep += tab(indent+1) + self.event.display(indent+1)
        rep += tab(indent+1) + "args(\n"
        for arg in self.args:
            rep += tab(indent+2) + arg + "\n"
        rep += tab(indent+1) + ")\n"
        rep += tab(indent+1) + self.block.display(indent+1)
        rep += tab(indent) + ")\n"

        return rep

class SendStm(Stm):
    def __init__(self, event, args):
        self.event = event
        self.args = args

    def run(self, env):
        event = self.event.run(env)
        if type(event) == Event:
            key = event.get_key()
        else:
            key = event
        env.trigger(key, {key: val for key, val in [arg.run(env) for arg in self.args]})

    def display(self, indent=0):
        rep = "SendStm(\n"
        rep += tab(indent+1) + self.event.display(indent+1)
        rep += tab(indent+1) + "args(\n"
        for arg in self.args:
            rep += tab(indent+2) + arg.display(indent+2)
        rep += tab(indent+1) + ")\n"
        rep += tab(indent) + ")\n"

        return rep

class ExpStm(Stm):
    def __init__(self, exp):
        self.exp = exp

    def run(self, env):
        self.exp.run(env)

    def display(self, indent=0):
        rep = "ExpStm(\n"
        rep += tab(indent+1) + (self.exp.display(indent+1) if self.exp else "None") + "\n"
        rep += tab(indent) + ")\n"

        return rep

class Exp(Node):
    def __init__(self):
        pass

    def run(self, env):
        pass

    def display(self, indent=0):
        return tab(indent) + "Exp()\n"

class NumExp(Exp):
    def __init__(self, num):
        self.num = num

    def run(self, env):
        return self.num

    def display(self, indent=0):
        rep = "NumExp(\n"
        rep += tab(indent+1) + str(self.num) + "\n"
        rep += tab(indent) + ")\n"

        return rep

class IdExp(Exp):
    def __init__(self, id):
        self.id = id

    def run(self, env):
        return env.scope.lookup(self.id)

    def display(self, indent=0):
        rep = "IdExp(\n"
        rep += tab(indent+1) + self.id + "\n"
        rep += tab(indent) + ")\n"

        return rep

class StrExp(Exp):
    def __init__(self, str):
        self.str = str

    def run(self, env):
        return self.str

    def display(self, indent=0):
        rep = "StrExp(\n"
        rep += tab(indent+1) + self.str + "\n"
        rep += tab(indent) + ")\n"

        return rep

class OpExp(Exp):
    def __init__(self, op, exp1, exp2):
        self.op = op
        self.exp1 = exp1
        self.exp2 = exp2

    def run(self, env):
        if self.op == Token.MUL:
            return self.exp1.run(env) * self.exp2.run(env)
        elif self.op == Token.DIV:
            return self.exp1.run(env) / self.exp2.run(env)
        elif self.op == Token.ADD:
            return self.exp1.run(env) + self.exp2.run(env)
        elif self.op == Token.SUB:
            return self.exp1.run(env) - self.exp2.run(env)
        elif self.op == Token.GT:
            return self.exp1.run(env) > self.exp2.run(env)
        elif self.op == Token.LT:
            return self.exp1.run(env) < self.exp2.run(env)
        elif self.op == Token.AND:
            return self.exp1.run(env) and self.exp2.run(env)
        elif self.op == Token.OR:
            return self.exp1.run(env) or self.exp2.run(env)

    def display(self, indent=0):
        rep = "OpExp(\n"
        rep += tab(indent+1) + str(self.op) + "\n"
        rep += tab(indent+1) + self.exp1.display(indent+1)
        rep += tab(indent+1) + self.exp2.display(indent+1)
        rep += tab(indent) + ")\n"

        return rep

class UnaryOpExp(Exp):
    def __init__(self, op, exp):
        self.op = op
        self.exp = exp

    def run(self, env):
        if self.op == Token.SUB:
            return -self.exp.run(env)
        elif self.op == Token.NOT:
            return not self.exp.run(env)

    def display(self, indent=0):
        rep = "UnaryOpExp(\n"
        rep += tab(indent+1) + str(self.op) + "\n"
        rep += tab(indent+1) + self.exp.display(indent+1)
        rep += tab(indent) + ")\n"

        return rep

class ProcExp(Exp):
    def __init__(self, proc, args):
        self.proc = proc
        self.args = args

    def run(self, env):
        args = [arg.run(env) for arg in self.args]
        if config["debug"] and config["verbose"]:
            print("PROC", self.proc, args)
        if self.proc == Token.ENTITY:
            entity = env.level.entity_type_map[args[0]](env.level, Vec(args[1], args[2]))
            env.level.add_entity(entity)
            return entity
        elif self.proc == Token.SURFACE:
            surface = Surface(Vec(args[0], args[1]), Vec(args[2], args[3]))
            env.level.add_surface(surface)
            return surface
        elif self.proc == Token.BACKGROUND:
            background = Platform(args[0], Vec(args[1], args[2]), args[3], args[4], args[5], Vec(args[6], args[7]))
            env.level.add_background(background)
            return background
        elif self.proc == Token.TEXTURE:
            env.level.load_texture(args[0], args[1])
            return None

    def display(self, indent=0):
        rep = "ProcExp(\n"
        rep += tab(indent+1) + str(self.proc) + "\n"
        rep += tab(indent+1) + "args(\n"
        for arg in self.args:
            rep += tab(indent+2) + arg.display(indent+2)
        rep += tab(indent+1) + ")\n"
        rep += tab(indent) + ")\n"

        return rep

class EventExp(Exp):
    def __init__(self, event, target):
        self.event = event
        self.target = target

    def run(self, env):
        return Event(self.event, self.target.run(env))

    def display(self, indent=0):
        rep = "EventExp(\n"
        rep += tab(indent+1) + str(self.event) + " @ " + self.target.display(indent+1)
        rep += tab(indent) + ")\n"

        return rep

class ParamExp(Exp):
    def __init__(self, var, exp):
        self.var = var
        self.exp = exp

    def run(self, env):
        return self.var, self.exp.run(env)

    def display(self, indent=0):
        rep = "ParamExp(\n"
        rep += tab(indent+1) + self.var + "\n"
        rep += tab(indent+1) + self.exp.display(indent+1)
        rep += tab(indent) + ")\n"

        return rep