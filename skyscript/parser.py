from enum import Enum, auto
from config import config
from skyscript.ast import *
from skyscript.lexer import Lexer, Token

class Type(Enum):
    NUMERICAL = auto()
    STRING = auto()
    BOOLEAN = auto()

class Parser:
    def __init__(self):
        self.index = 0
        self.tokens = []

    def __assert(self, actual, expected):
        if actual != expected:
            raise SyntaxError("Expected %s got %s at %i" % (expected, actual, self.index))

    def __type_assert(self, actual, expected):
        if expected == Type.STRING and type(actual) == str:
            pass
        elif expected == Type.NUMERICAL and type(actual) in (int, float):
            pass
        elif expected == Type.BOOLEAN and type(actual) == bool:
            pass
        else:
            raise SyntaxError("Expected %s got %s at %i" % (expected, type(actual), self.index))

    def __eat(self):
        if self.index < len(self.tokens):
            self.index += 1
            token = self.tokens[self.index - 1]
            if config["debug"] and config["verbose"]:
                print("%i:" % (self.index), token[0], token[1])
            return token
        else:
            return None, None

    def __look(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        else:
            return None, None

    def __parse_keyword(self):
        token, value = self.__eat()

        if token == Token.TEXTURE:
            name = self.__parse_exp()
            path = self.__parse_exp()

            return ProcExp(token, [name, path])
        elif token == Token.BACKGROUND:
            name = self.__parse_exp()
            x = self.__parse_exp()
            y = self.__parse_exp()
            width = self.__parse_exp()
            height = self.__parse_exp()

            return ProcExp(token, [name, x, y, width, height])
        elif token == Token.SURFACE:
            x1 = self.__parse_exp()
            y1 = self.__parse_exp()
            x2 = self.__parse_exp()
            y2 = self.__parse_exp()

            return ProcExp(token, [x1, y1, x2, y2])
        elif token == Token.ENTITY:
            name = self.__parse_exp()
            x = self.__parse_exp()
            y = self.__parse_exp()

            return ProcExp(token, [name, x, y])

    def __parse_factor(self):
        token, value = self.__look()

        if token == Token.NUM:
            self.__eat()

            return NumExp(int(value))
        elif token == Token.ID:
            self.__eat()

            token, _ = self.__look()
            if token == Token.DOT:
                pass
            elif token == Token.AT:
                self.__eat()
                token, target_value = self.__eat()
                self.__assert(token, Token.ID)

                return EventExp(value, IdExp(target_value))
            else:
                return IdExp(value)

        elif token == Token.STRING:
            self.__eat()

            return StrExp(value)
        elif token == Token.LPAR:
            self.__eat()
            exp = self.__parse_exp()
            token, _ = self.__eat()

            self.__assert(token, Token.RPAR)

            return exp
        elif token == Token.SUB:
            self.__eat()
            exp = self.__parse_exp()

            return UnaryOpExp(token, exp)
        elif token == Token.NOT:
            self.__eat()
            exp = self.__parse_exp()

            return UnaryOpExp(token, exp)
        else:
            return self.__parse_keyword()

    def __parse_term(self):
        factor = self.__parse_factor()

        token, _ = self.__look()
        if token == Token.MUL or token == Token.DIV:
            self.__eat()
            factor2 = self.__parse_factor()

            return OpExp(token, factor, factor2)
        else:
            return factor

    def __parse_arithmetic(self):
        term = self.__parse_term()

        token, _ = self.__look()

        if token == Token.ADD or token == Token.SUB:
            self.__eat()
            term2 = self.__parse_term()

            return OpExp(token, term, term2)
        else:
            return term

    def __parse_exp(self):
        term = self.__parse_arithmetic()

        token, _ = self.__look()

        if token == Token.GT or token == Token.LT:
            self.__eat()
            term2 = self.__parse_arithmetic()

            return OpExp(token, term, term2)
        elif token == Token.AND or token == Token.OR:
            self.__eat()
            term2 = self.__parse_exp()

            return OpExp(token, term, term2)
        else:
            return term

    def __parse_on(self):
        self.__eat()

        event_name = self.__parse_exp()
        params = []

        token, _ = self.__eat()
        if token == Token.WITH:
            while self.__look()[0] != Token.DO:
                token, value = self.__eat()
                self.__assert(token, Token.ID)
                params.append(value)

        token, value = self.__look()

        self.__assert(token, Token.DO)

        block = self.__parse_block()
        return OnStm(event_name, params, block)

    def __parse_if(self):
        self.__eat()

        exp = self.__parse_exp()

        block = self.__parse_block()

        return IfStm(exp, block)

    def __parse_let(self):
        self.__eat()

        token, var = self.__eat()
        self.__assert(token, Token.ID)

        token, _ = self.__eat()
        self.__assert(token, Token.COLON)

        exp = self.__parse_exp()

        # self.env.insert(var, exp)

        return LetStm(var, exp)

    def __parse_send(self):
        self.__eat()

        event = self.__parse_exp()
        params = []

        if self.__look()[0] == Token.WITH:
            self.__eat()
            token, param_name = self.__eat()
            while token != Token.END:
                self.__assert(token, Token.ID)
                self.__assert(self.__eat()[0], Token.COLON)
                param_val = self.__parse_exp()

                params.append(ParamExp(param_name, param_val))

                token, param_name = self.__eat()
        
        return SendStm(event, params)

    def __parse_block(self):
        self.__eat()

        stms = []

        while self.__look()[0] != Token.END:
            stms.append(self.__parse_stm())

        self.__eat()

        return Block(stms)

    def __parse_stm(self):
        token, _ = self.__look()

        if token == Token.LET:
            return self.__parse_let()
        elif token == Token.IF:
            return self.__parse_if()
        elif token == Token.ON:
            return self.__parse_on()
        elif token == Token.SEND:
            return self.__parse_send()
        else:
            return ExpStm(self.__parse_exp())

    def __parse(self):
        stms = []
        while self.index < len(self.tokens):
            stms.append(self.__parse_stm())

        return Prog(Block(stms))

    def parse(self, tokens):
        self.tokens = tokens
        ast = self.__parse()
        if config["debug"] and config["verbose"]:
            print(ast.display())

        return ast
