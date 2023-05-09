import utils
import lexer
import parser

inbuf = utils.loadFile("tests/testParser.c")

tokens = lexer.tokenize(inbuf)

# lexer.showTokens(tokens)

parser.parse(tokens)