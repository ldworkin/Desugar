#!/usr/bin/env python

import sys
from pyparsing import *

def desugar(string):

    valid_chars = alphanums + ",()[]<>="

    do = Literal("do").suppress()
    lbracket = Literal("{").suppress()
    rbracket = Literal("}").suppress()
    get = Literal("<-").suppress()
    semicolon = Literal(";").suppress()

    exp = OneOrMore(Word(valid_chars))
    exp.setParseAction(lambda tokens: " ".join(tokens))
    stmt = Group(Word(valid_chars) + get + exp)
    stmts = Forward()
    case1 = exp + semicolon + stmts
    case1.setParseAction(lambda tokens: tokens[0] + " >> " + tokens[1])
    case2 = stmt + semicolon + stmts
    case2.setParseAction(lambda tokens: tokens[0][1] + " >>= (\\" + 
                                        tokens[0][0] + " -> " + 
                                        tokens[1] + ")")
    stmts << (case1 | case2 | exp)
    grammar = do + lbracket + stmts + rbracket

    try:
        return "".join(grammar.parseString(string))
    except ParseException:
        return "Bad syntax."

if len(sys.argv) < 2:
    print desugar(raw_input("Enter a do block: "))
else:
    print desugar(sys.argv[1])





