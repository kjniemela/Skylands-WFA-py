def tab(indent):
    return indent * "  "

class Node:
    def __init__(self):
        pass

    def run(self):
        pass

    def display(self, indent=0):
        return tab(indent) + "Node()\n"

class Block(Node):
    def __init__(self, stms):
        self.stms = stms

    def run(self):
        for stm in self.stms:
            stm.run()

    def display(self, indent=0):
        rep = "Block(\n"
        for stm in self.stms:
            rep += tab(indent+1) + stm.display(indent+1)
        rep += tab(indent) + ")\n"

        return rep

class Prog(Node):
    def __init__(self, block):
        self.block = block

    def run(self):
        self.block.run()

    def display(self, indent=0):
        rep = "Prog(\n"
        rep += tab(indent+1) + self.block.display(indent+1)
        rep += tab(indent) + ")\n"

        return rep

class Stm(Node):
    def __init__(self):
        pass

    def run(self):
        pass

    def display(self, indent=0):
        return tab(indent) + "Stm()\n"

class LetStm(Stm):
    def __init__(self, var, exp):
        self.var = var
        self.exp = exp

    def run(self):
        pass

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

    def run(self):
        if self.exp.run():
            return self.block.run()

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

    def run(self):
        pass

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

    def run(self):
        pass

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

    def run(self):
        self.exp.run()

    def display(self, indent=0):
        rep = "ExpStm(\n"
        rep += tab(indent+1) + (self.exp.display(indent+1) if self.exp else "None") + "\n"
        rep += tab(indent) + ")\n"

        return rep

class Exp(Node):
    def __init__(self):
        pass

    def run(self):
        pass

    def display(self, indent=0):
        return tab(indent) + "Exp()\n"

class NumExp(Exp):
    def __init__(self, num):
        self.num = num

    def run(self):
        return self.num

    def display(self, indent=0):
        rep = "NumExp(\n"
        rep += tab(indent+1) + str(self.num) + "\n"
        rep += tab(indent) + ")\n"

        return rep

class IdExp(Exp):
    def __init__(self, id):
        self.id = id

    def run(self):
        pass

    def display(self, indent=0):
        rep = "IdExp(\n"
        rep += tab(indent+1) + self.id + "\n"
        rep += tab(indent) + ")\n"

        return rep

class StrExp(Exp):
    def __init__(self, str):
        self.str = str
        pass

    def run(self):
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

    def run(self):
        if op == Token.MUL:
            return exp1.run() * exp2.run()
        elif op == Token.DIV:
            return exp1.run() / exp2.run()
        elif op == Token.ADD:
            return exp1.run() + exp2.run()
        elif op == Token.SUB:
            return exp1.run() - exp2.run()
        elif op == Token.GT:
            return exp1.run() > exp2.run()
        elif op == Token.LT:
            return exp1.run() < exp2.run()

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

    def run(self):
        if op == Token.SUB:
            return -exp.run()
        elif op == Token.NOT:
            return not exp.run()

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

    def run(self):
        pass

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

    def run(self):
        pass

    def display(self, indent=0):
        rep = "EventExp(\n"
        rep += tab(indent+1) + str(self.event) + " @ " + str(self.target) + "\n"
        rep += tab(indent) + ")\n"

        return rep

class ParamExp(Exp):
    def __init__(self, var, exp):
        self.var = var
        self.exp = exp

    def run(self):
        pass

    def display(self, indent=0):
        rep = "ParamExp(\n"
        rep += tab(indent+1) + self.var + "\n"
        rep += tab(indent+1) + self.exp.display(indent+1)
        rep += tab(indent) + ")\n"

        return rep