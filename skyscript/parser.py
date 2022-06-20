from enum import Enum, auto
from ast import *  ## TODO - imports need to be fixed for prod
from lookuptable import LookupTable
from lexer import Lexer, Token

class Event:
    def __init__(self, event, target):
        self.event = event
        self.target = target

    def __repr__(self):
        return "Event(%s @ %s)" % (self.event, self.target)

class Type(Enum):
    NUMERICAL = auto()
    STRING = auto()
    BOOLEAN = auto()

class Parser:
    def __init__(self):
        self.index = 0
        self.tokens = []

        self.env = LookupTable()

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
            # print("%i:" % (self.index), token[0], token[1])
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

            # self.__type_assert(name, Type.STRING)
            # self.__type_assert(path, Type.STRING)

            # print("TODO HOOKUP TEXTURE LOADER", name, path)

            return ProcExp(token, [name, path])
        elif token == Token.BACKGROUND:
            name = self.__parse_exp()
            x = self.__parse_exp()
            y = self.__parse_exp()
            width = self.__parse_exp()
            height = self.__parse_exp()
            direction = self.__parse_exp()

            # self.__type_assert(name, Type.STRING)
            # self.__type_assert(x, Type.NUMERICAL)
            # self.__type_assert(y, Type.NUMERICAL)
            # self.__type_assert(width, Type.NUMERICAL)
            # self.__type_assert(height, Type.NUMERICAL)
            # self.__type_assert(direction, Type.NUMERICAL)

            # print("TODO HOOKUP BACKG LOADER", name, x, y, width, height, direction)

            return ProcExp(token, [name, x, y, width, height, direction])
        elif token == Token.SURFACE:
            x1 = self.__parse_exp()
            y1 = self.__parse_exp()
            x2 = self.__parse_exp()
            y2 = self.__parse_exp()

            # self.__type_assert(x1, Type.NUMERICAL)
            # self.__type_assert(y1, Type.NUMERICAL)
            # self.__type_assert(x2, Type.NUMERICAL)
            # self.__type_assert(y2, Type.NUMERICAL)

            # print("TODO HOOKUP SURF LOADER", x1, y1, x2, y2)

            return ProcExp(token, [x1, y1, x2, y2])
        elif token == Token.ENTITY:
            name = self.__parse_exp()
            x = self.__parse_exp()
            y = self.__parse_exp()

            # self.__type_assert(name, Type.STRING)
            # self.__type_assert(x, Type.NUMERICAL)
            # self.__type_assert(y, Type.NUMERICAL)

            # print("TODO HOOKUP ENTITY LOADER", name, x, y)

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
                # self.__eat()
                # token, _ = self.__eat()
                # self.__assert(token, Token.ID)
                # return self.env.lookup(value)
                pass
            elif token == Token.AT:
                self.__eat()
                token, target_value = self.__eat()
                self.__assert(token, Token.ID)
                return Event(value, target_value)
            else:
                return self.env.lookup(value)

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

            # self.__type_assert(exp, Type.NUMERICAL)

            return UnaryOpExp(token, exp)
        elif token == Token.NOT:
            self.__eat()
            exp = self.__parse_exp()

            # self.__type_assert(exp, Type.BOOLEAN)

            return UnaryOpExp(token, exp)
        else:
            return self.__parse_keyword()

    def __parse_term(self):
        factor = self.__parse_factor()

        token, _ = self.__look()
        if token == Token.MUL or token == Token.DIV:
            self.__eat()
            factor2 = self.__parse_factor()

            # self.__type_assert(factor, Type.NUMERICAL)
            # self.__type_assert(factor2, Type.NUMERICAL)

            return OpExp(token, factor, factor2)
        else:
            return factor

    def __parse_arithmetic(self):
        term = self.__parse_term()

        token, _ = self.__look()

        if token == Token.ADD or token == Token.SUB:
            self.__eat()
            term2 = self.__parse_term()

            # self.__type_assert(term, Type.NUMERICAL)
            # self.__type_assert(term2, Type.NUMERICAL)

            return OpExp(token, term, term2)
        else:
            return term

    def __parse_exp(self):
        term = self.__parse_arithmetic()

        token, _ = self.__look()

        if token == Token.GT or token == Token.LT:
            self.__eat()
            term2 = self.__parse_arithmetic()

            # self.__type_assert(term, Type.NUMERICAL)
            # self.__type_assert(term2, Type.NUMERICAL)

            return OpExp(token, term, term2)
        elif token == Token.AND or token == Token.OR:
            self.__eat()
            term2 = self.__parse_arithmetic()

            # self.__type_assert(term, Type.BOOLEAN)
            # self.__type_assert(term2, Type.BOOLEAN)

            return OpExp(token, term, term2)
        else:
            return term

    def __parse_on(self):
        self.__eat()

        event_name = self.__parse_exp()
        params = []

        token, _ = self.__eat()
        if token == Token.WITH:
            token, value = self.__eat()
            while token != Token.DO:
                self.__assert(token, Token.ID)
                params.append(IdExp(value))

                token, value = self.__eat()

        self.__assert(token, Token.DO)

        print("ON %s WITH %s DO" % (event_name, str(params)))

        return OnStm(event_name, params)

        print(self.env)
        self.env.push_scope()
        print(self.env)

        for param in params: ## TODO - this should not be here!
            self.env.insert(param, 0)

        self.__run_block()
        self.env.pop_scope()
        print(self.env)

    def __parse_if(self):
        self.__eat()

        exp = self.__parse_exp()

        print("IF %s" % (str(exp)))

        block = self.__parse_block()

        return IfStm(exp, block)
        # if boolean:
        #     self.__run_block()
        # else:
        #     self.__skip_block()

    def __parse_let(self):
        self.__eat()

        token, var = self.__eat()
        self.__assert(token, Token.ID)

        token, _ = self.__eat()
        self.__assert(token, Token.COLON)

        exp = self.__parse_exp()

        self.env.insert(var, exp)

        return LetStm(var, exp)

    def __parse_send(self):
        self.__eat()

        event = self.__parse_exp()
        #params = {}
        params = []

        if self.__look()[0] == Token.WITH:
            self.__eat()
            token, param_name = self.__eat()
            while token != Token.END:
                self.__assert(token, Token.ID)
                self.__assert(self.__eat()[0], Token.COLON)
                param_val = self.__parse_exp()

                #params[param_name] = param_val
                params.append(param_val)

                token, param_name = self.__eat()

        print("SEND %s TO %s" % (params, event))

        return SendStm(event, params)

    def __parse_block(self):
        self.__eat()

        while self.__look()[0] != Token.END:
            self.__parse_stm()

        self.__eat()

    def __skip_block(self):
        self.__eat()
        print("SKIP BLOCK")
        depth = 1
        last_open = None

        token, _ = self.__look()
        while token != None and depth > 0:
            self.__eat()

            if token == Token.DO and last_open == Token.WITH:
                depth -= 1

            if token == Token.END:
                depth -= 1
            elif token in (
                Token.ON,
                Token.IF,
                Token.WITH,
            ):
                last_open = token
                depth += 1

            token, _ = self.__look()


        print("EXIT SKIP")

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
        print(tokens)
        print(self.__parse().display())

parser = Parser()
lexer = Lexer()
src = """
texture "jungle2" "levels/narbadhir1/jungle2.png"
background "jungle2" 0 0 1067 527 0

let surf1 : surface 200 (-200) 200 (-200)
surface 200 (-200) 200 0

let test : (1 + 2)

let entity1 : entity "shoaldier" 100 (-160)

send "spawn" with
    x : 0
    y : (-100)
end

on hurt @ entity1 with damage do
  let a : (1 + 2) * 5
  let x : 100

  if damage < x then
    send "slide_door" with
      door : surf1
      speed : 100 + damage
    end
  end
  send "play_sound" with sound : "ouch" end
  send "test_event"
end

send hurt @ entity1 with damage : 0 end
send hurt @ entity1 with damage : 120 end

let test2 : hurt @ entity1
let x : 1
"""
parser.parse(lexer.tokenize(src))