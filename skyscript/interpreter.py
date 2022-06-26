from config import config
from vec import Vec

from skyscript.lexer import Lexer
from skyscript.parser import Parser
from skyscript.lookuptable import LookupTable
from skyscript.ast import Event

class BuiltinEvent:
    def __init__(self, func):
        self.func = func

    def trigger(self, env, kwargs):
        self.func(kwargs)

class Interpreter:
    def __init__(self, level):
        self.parser = Parser()
        self.lexer = Lexer()
        self.level = level
        self.ast = None

        self.funcs = {
            "spawn": BuiltinEvent(self.__builtin_spawn),
            "config": BuiltinEvent(self.__builtin_config),
        }

        self.scope = LookupTable()

    def __builtin_spawn(self, kwargs):
        self.level.player.set_spawn(Vec(**kwargs))

    def __builtin_config(self, kwargs):
        for key in kwargs:
            config[key] = bool(kwargs[key])

    def add_func(self, event, stm):
        if type(event) == Event:
            key = event.get_key()
        else:
            key = event
        self.funcs[key] = stm

    def trigger(self, event, args):
        if event in self.funcs:
            self.funcs[event].trigger(self, args)
        else:
            if config["debug"] and config["verbose"]:
                print("MISSING FUNC:", event)

    def load(self, src):
        self.ast = self.parser.parse(self.lexer.tokenize(src))

    def run(self):
        self.ast.run(self)
        # print(self.scope)
        # print(self.funcs)