from skyscript.lexer import Lexer
from skyscript.parser import Parser


class Interpreter:
    def __init__(self, level):
        self.parser = Parser()
        self.lexer = Lexer()
        self.level = level

    def load(self, src):
        self.parser.parse(self.lexer.tokenize(src))