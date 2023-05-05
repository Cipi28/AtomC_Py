import utils

tokens = []  # single linked list of tokens
line = 1  # current line in the input file


class Token:
    def __init__(self):
        self.line = None
        self.code = None
        self.val = None


def addTk(code):
    global tokens
    global line
    tk = Token()
    tk.line = line
    tk.code = code
    tokens.append(tk)
    return tk


def tokenize(pch):
    global line
    global tokens
    index = 0
    while True:
        if index == len(pch):
            addTk("END")
            return tokens
        elif pch[index] == '\t' or pch[index] == ' ':
            index += 1
        elif pch[index] == '\r':
            if index < len(pch) - 1 and pch[index + 1] == '\n':
                index += 2
            else:
                index += 1
        elif pch[index:index + 2] == "//":
            index += 2
            while pch[index] not in "\n\r\0":
                index += 1
        elif pch[index] == '\n':
            index += 1
            line += 1
        elif pch[index] == ',':
            addTk("COMMA")
            index += 1
        elif pch[index] == ';':
            addTk("SEMICOLON")
            index += 1
        elif pch[index] == '(':
            addTk("LPAR")
            index += 1
        elif pch[index] == ')':
            addTk("RPAR")
            index += 1
        elif pch[index] == '[':
            addTk("LBRACKET")
            index += 1
        elif pch[index] == ']':
            addTk("RBRACKET")
            index += 1
        elif pch[index] == '{':
            addTk("LACC")
            index += 1
        elif pch[index] == '}':
            addTk("RACC")
            index += 1
        elif pch[index] == '\0':
            addTk("END")
            return tokens
        elif pch[index] == '+':
            addTk("ADD")
            index += 1
        elif pch[index] == '-':
            addTk("SUB")
            index += 1
        elif pch[index] == '*':
            addTk("MUL")
            index += 1
        elif pch[index] == '/':
            addTk("DIV")
            index += 1
        elif pch[index] == '.':
            addTk("DOT")
            index += 1
        elif pch[index] == '&' and pch[index + 1] == '&':
            addTk("AND")
            index += 2
        elif pch[index] == '|' and pch[index + 1] == '|':
            addTk("OR")
            index += 2
        elif pch[index] == '!':
            if index < len(pch) - 1 and pch[index + 1] == '=':
                addTk("NOTEQ")
                index += 2
            else:
                addTk("NOT")
                index += 1
        elif pch[index] == '=':
            if index < len(pch) - 1 and pch[index + 1] == '=':
                addTk("EQUAL")
                index += 2
            else:
                addTk("ASSIGN")
                index += 1
        elif pch[index] == '<':
            if index < len(pch) - 1 and pch[index + 1] == '=':
                addTk("LESSEQ")
                index += 2
            else:
                addTk("LESS")
                index += 1
        elif pch[index] == '>':
            if index < len(pch) - 1 and pch[index + 1] == '=':
                addTk("GREATEREQ")
                index += 2
            else:
                addTk("GREATER")
                index += 1
        elif pch[index].isalpha() or pch[index] == '_':
            start = index
            index += 1
            while index < len(pch) and (pch[index] == '_' or pch[index].isalnum()):
                index += 1
            text = pch[start:index]
            if text == 'char':
                addTk("TYPE_CHAR")
            elif text == 'double':
                addTk("TYPE_DOUBLE")
            elif text == 'else':
                addTk("ELSE")
            elif text == 'if':
                addTk("IF")
            elif text == 'int':
                addTk("TYPE_INT")
            elif text == 'return':
                addTk("RETURN")
            elif text == 'struct':
                addTk("STRUCT")
            elif text == 'void':
                addTk("VOID")
            elif text == 'while':
                addTk("WHILE")
            else:
                tk = addTk("ID")
                tk.val = text
        elif pch[index].isdigit():
            start = index
            index += 1
            while index < len(pch) and (pch[index].isalnum() or pch[index] in "-+.eE"):
                if pch[index] in "-+" and (not pch[index - 1] in "eE"):
                    break
                index += 1
            text = pch[start:index]
            if all(c.isdigit() for c in text):
                tk = addTk("INT")
                tk.val = int(text)
            elif checkIfDouble(text):
                tk = addTk("DOUBLE")
                tk.val = float(text)
            else:
                utils.err(f"Not valid double on line {line}")
        elif pch[index] == "'" and pch[index + 1] != "'" and pch[index + 2] == "'":
            tk = addTk("CHAR")
            tk.val = pch[index + 1]
            index = index + 3
        elif pch[index] == '"':
            index += 1
            start = index
            while index < len(pch) and pch[index] != '"':
                index += 1
            text = pch[start:index]
            index += 1
            tk = addTk("STRING")
            tk.val = text

        else:
            utils.err(f"invalid char: {pch[index]} ({ord(pch[index])})")


def checkIfDouble(text):
    if not text or not text[0].isdigit() or text.count('.') > 1 or (text.count('e') + text.count('E')) > 1:
        return False

    # Check if string has more than one decimal point
    decimal = False
    i = 1
    while i < len(text):
        if text[i] == '.':
            if decimal:
                return False
            decimal = True
        elif not text[i].isdigit():
            break
        i += 1

    # Check if string has more than one exponent
    i = 1
    exponent = False
    while i < len(text):
        if i < len(text) and text[i] in ('e', 'E'):
            if exponent:
                return False
            exponent = True
            j = i + 1
            if j < len(text) and text[j] in ('+', '-'):
                if j+1 == len(text) or not text[j+1].isdigit():
                    return False
        i += 1
    return True


def showTokens(tokens):
    for token in tokens:
        if token.val is not None:
            print(str(token.line).ljust(6) + token.code + ":" + str(token.val))
        else:
            print(str(token.line).ljust(6) + token.code)

        # print(tk.line, "  ", tk.code)
        # print("   ")
        # print(tk.code)
