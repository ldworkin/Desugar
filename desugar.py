#!/usr/bin/env python

'''
DESCRIPTION:

A tiny Python script to expand or "desugar" Haskell do blocks. 

You can also ask lambdabot on the IRC channel to @undo expressions;
this was written mostly for my own understanding, and with the
intention of expanding the functionality later.

As of now, the capabilities are very limited. Most notably,
you cannot use pure code in the do blocks (such as let statements). 

DEPENDENCIES:

Pyparsing (http://pyparsing.wikispaces.com/)

USAGE:

Provide the do block as the first (and only) command line argument. 
If no arguments are provided, you will be prompted for input.

EXAMPLES:

do { x1 <- eval x; x2 <- eval y; safediv x1 x2 } ==
eval x >>= (\\x1 -> eval y >>= (\\x2 -> safediv x1 x2))

do { x <- xs; y <- ys; return (x,y) } ==
xs >>= (\\x -> ys >>= (\\y -> return (x,y)))

do { x <- getChar ; y <- getChar; print [x,y]; return True } ==
getChar >>= (\\x -> getChar >>= (\\y -> print [x,y] >> return True))

'''

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





