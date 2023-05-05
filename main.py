import utils
import lexer
import parser

inbuf = utils.loadFile("tests/testLex.c")

tokens = lexer.tokenize(inbuf)

lexer.showTokens(tokens)

parser.parse(tokens)
