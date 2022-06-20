from enum import Enum, auto

class Token(Enum):
    ID = auto()
    STRING = auto()
    NUM = auto()

    # Parentheses
    LPAR = auto()
    RPAR = auto()

    # Operators
    MUL = auto()
    DIV = auto()
    ADD = auto()
    SUB = auto()

    AT = auto()

    # Punctuation
    COLON = auto()
    DOT = auto()
    NL = auto()

    # Keywords
    ON = auto()
    IF = auto()
    SEND = auto()
    WITH = auto()
    DO = auto()
    THEN = auto()
    END = auto()
    LET = auto()

    # Reserved identifiers
    ENTITY = auto()
    SURFACE = auto()
    TEXTURE = auto()
    BACKGROUND = auto()

class Lexer:
    def __init__(self):
        self.index = 0
        self.value = ""
        self.tokens = []
        self.src = ""

    def __assert(self, actual, expected):
        if actual != expected:
            raise SyntaxError

    def __eat(self):
        if self.index < len(self.src):
            self.index += 1
            self.value += self.src[self.index - 1]
            return self.src[self.index - 1]
        else:
            return None

    def __look(self):
        if self.index < len(self.src):
            return self.src[self.index]
        else:
            return None

    def __push(self, type):
        self.tokens.append((type, self.value))
        self.value = ""

    def __lex_func(self, fn, type=None):
        while self.index < len(self.src) and fn(self.__look()):
            self.__eat()

        if type != None:
            self.__push(type)

    def tokenize(self, src):
        self.index = 0
        self.tokens = []
        self.src = src

        while self.index < len(src):
            char = self.__eat()
            if char.isalpha():
                self.__lex_func(lambda c: c.isalnum() or c == '_')
                if self.value == "on":
                    self.__push(Token.ON)
                elif self.value == "if":
                    self.__push(Token.IF)
                elif self.value == "send":
                    self.__push(Token.SEND)
                elif self.value == "with":
                    self.__push(Token.WITH)
                elif self.value == "do":
                    self.__push(Token.DO)
                elif self.value == "then":
                    self.__push(Token.THEN)
                elif self.value == "end":
                    self.__push(Token.END)
                elif self.value == "let":
                    self.__push(Token.LET)
                elif self.value == "entity":
                    self.__push(Token.ENTITY)
                elif self.value == "surface":
                    self.__push(Token.SURFACE)
                elif self.value == "texture":
                    self.__push(Token.TEXTURE)
                elif self.value == "background":
                    self.__push(Token.BACKGROUND)
                else:
                    self.__push(Token.ID)
            elif char == '"':
                self.value = ""
                self.__lex_func(lambda c: c != '"')
                self.__push(Token.STRING)
                token = self.__eat()
                self.__assert(token, '"')
                self.value = ""
            elif char.isdigit():
                self.__lex_func(lambda c: c.isdigit(), Token.NUM)
            elif char == '(':
                self.__push(Token.LPAR)
            elif char == ')':
                self.__push(Token.RPAR)
            elif char == '*':
                self.__push(Token.MUL)
            elif char == '/':
                self.__push(Token.DIV)
            elif char == '+':
                self.__push(Token.ADD)
            elif char == '-':
                self.__push(Token.SUB)
            elif char == ':':
                self.__push(Token.COLON)
            elif char == '.':
                self.__push(Token.DOT)
            elif char == '@':
                self.__push(Token.AT)
            elif char == '\n':
                self.value = ""
                # self.__push(Token.NL)
            elif char.isspace():
                self.value = ""
            else:
                print("[Lexing Error] Unknown char: '" + char + "'")

        return self.tokens