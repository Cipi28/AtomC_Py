import utils
import lexer
import parser

inbuf = utils.loadFile("tests/testParse2.c")

tokens = lexer.tokenize(inbuf)

lexer.showTokens(tokens)

parser.parse(tokens)
# done pana la typeBase