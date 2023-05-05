import sys
import lexer

iTk = 0  # the iterator in the tokens list
tokens = []  # the list of tokens
consumedTk = lexer.Token  # the last consumed token

def tkerr(fmt, *args):
    sys.stderr.write("error in line %d: " % tokens[iTk].line)
    sys.stderr.write(fmt % args)
    sys.stderr.write("\n")
    sys.exit(1)

def consume(code):
    global iTk, tokens, consumedTk
    if tokens[iTk].code == code:
        consumedTk = tokens[iTk]
        iTk += 1
        return True
    return False

# structDef: STRUCT ID LACC varDef* RACC SEMICOLON
def structDef():
    global iTk
    start = iTk
    if consume("STRUCT"):
        if consume("ID"):
            if consume("LACC"):
                while True:
                    if varDef():
                        pass
                    else:
                        break
                if consume("RACC"):
                    if consume("SEMICOLON"):
                        return True
    iTk = start
    return False

# exprOr: exprOr OR exprAnd | exprAnd
# exprOr: exprAnd exprOrPrim
def exprOr():
    global iTk
    start = iTk
    if exprAnd():
        if exprOrPrim():
            return True
    iTk = start
    return False

# exprPrimary: ID ( LPAR ( expr ( COMMA expr )* )? RPAR )? | INT | DOUBLE | CHAR | STRING | LPAR expr RPAR
def exprPrimary():
    global iTk
    start = iTk
    if consume("ID"):
        if consume("LPAR"):
            if expr():
                while True:
                    if consume("COMMA"):
                        if expr():
                            pass
                        else:
                            # semnalat eroare
                            break
                    else:
                        break
            if consume("RPAR"):
                    return True
            else:
                tkerr("lipseste expresia")
        else:
            return True
    if consume("INT"):
        return True
    if consume("DOUBLE"):
        return True
    if consume("CHAR"):
        return True
    if consume("STRING"):
        return True
    if consume("LPAR"):
        if expr():
            if consume("RPAR"):
                return True
    iTk = start
    return False


# exprUnary: ( SUB | NOT ) exprUnary | exprPostfix
def exprUnary():
    global iTk
    start = iTk
    if consume("SUB"):
        if exprUnary():
            return True
    if consume("NOT"):
        if exprUnary():
            return True
    if exprPostfix():
        return True
    iTk = start
    return False


# exprCast: LPAR typeBase arrayDecl? RPAR exprCast | exprUnary
def exprCast():
    global iTk
    start = iTk
    if consume("LPAR"):
        if typeBase():
            if arrayDecl():
                pass
            if consume("RPAR"):
                if exprCast():
                    return True
    if exprUnary():
        return True
    iTk = start
    return False

#exprOr: exprOr OR exprAnd | exprAnd
#A: A α1 | … | A αm | β1 | … | β
#A = exprOr
#α1 = OR exprAnd
#β1 = exprAnd

#A: β1 A’ | … | βn A’
#EprOr: ExprAnd exprOrPrim

#A’: α1 A’ | … | αm A’ | ε (ε -> alternativa vida)
#ExprOrPrim: OR exprAnd ExprOrPrim | ε
#ExprOrPrim: (OR exprAnd ExprOrPrim)*


# exprAnd: exprAnd AND exprEq | exprEq
#A = exprAnd
#α1 = AND exprEq
#β1 = exprEq

#A: β1 A’ | … | βn A’
#EprAnd: ExprEq exprAndPrim

#A’: α1 A’ | … | αm A’ | ε (ε -> alternativa vida)
#ExprAndPrim: AND exprEq ExprAndPrim | ε
#ExprAndPrim: (AND exprEq ExprAndPrim)*
def exprAnd():

# ExprOrPrim: OR exprAnd ExprOrPrim | ε
def exprOrPrim():
    global iTk
    start = iTk
    if consume("OR"):
        if exprAnd():
            if exprOrPrim():
                return True
    iTk = start
    return True  # epsilon

# typeBase: TYPE_INT | TYPE_DOUBLE | TYPE_CHAR | STRUCT ID
def typeBase():
    global iTk
    start = iTk
    if consume("TYPE_INT"):
        return True
    if consume("TYPE_DOUBLE"):
        return True
    if consume("TYPE_CHAR"):
        return True
    if consume("STRUCT"):
        if consume("ID"):
            return True
        else:
            tkerr("lipseste numele structurii")  # de pus tot asa si pe structDef
    iTk = start
    return False

# varDef: typeBase ID arrayDecl? SEMICOLON
def varDef():
    global iTk
    start = iTk
    if typeBase():
        if consume("ID"):
            if arrayDecl():
                pass
            if consume("SEMICOLON"):
                return True
    iTk = start
    return False

# arrayDecl: LBRACKET INT? RBRACKET
def arrayDecl():
    global iTk
    start = iTk
    if consume("LBRACKET"):
        if consume("INT"):
            pass
        if consume("RBRACKET"):
            return True
    iTk = start
    return False

# fnDef: ( typeBase | VOID ) ID LPAR ( fnParam ( COMMA fnParam )* )? RPAR stmCompound
def fnDef():
    global iTk
    start = iTk
    if typeBase():
        pass
    elif consume("VOID"):
        pass
    else:
        tkerr("lipseste tipul de return al functiei") # de verificat daca e corecta
    if consume("ID"):
        if consume("LPAR"):
            if fnParam():
                while True:
                    if consume("COMMA"):
                        if fnParam():
                            pass
                        else:
                            break # eroare
                    else:
                        break # eroare
            if consume("RPAR"):
                if stmCompound():
                    return True
    iTk = start
    return False

# fnParam: typeBase ID arrayDecl?
def fnParam():
    global iTk
    start = iTk
    if typeBase():
        if consume("ID"):
            if arrayDecl():
                pass
            return True
    iTk = start
    return False

# stm: stmCompound | IF LPAR expr RPAR stm ( ELSE stm )? | WHILE LPAR expr RPAR stm | RETURN expr? SEMICOLON | expr? SEMICOLON
def stm():
    global iTk
    start = iTk
    if stmCompound():
        return True
    if consume("IF"):
        if consume("LPAR"):
            if expr():
                if consume("RPAR"):
                    if stm():
                        if consume("ELSE"):
                            if stm():
                                pass
                            else:
                                tkerr("something went wrong")
                        return True
    if consume("WHILE"):
        if consume("LPAR"):
            if expr():
                if consume("RPAR"):
                    if stm():
                        return True
    if consume("RETURN"):
        if expr():
            pass
        if consume("SEMICOLON"):
            return True
    if expr():
        pass
    if consume("SEMICOLON"):
        return True
    iTk = start
    return False

# stmCompound: LACC ( varDef | stm )* RACC
def stmCompound():
    global iTk
    start = iTk
    if consume("LACC"):
        while True:
            if varDef():
                pass
            elif stm():
                pass
            else:
                break
        if consume("RACC"):
            return True
    iTk = start
    return False

# expr: exprAssign
def expr():
    global iTk
    start = iTk
    if exprAssign():
        return True
    iTk = start
    return False

# exprAssign: exprUnary ASSIGN exprAssign | exprOr
def exprAssign():
    global iTk
    start = iTk
    if exprUnary():
        if consume("ASSIGN"):
            if exprAssign():
                return True
    iTk = start
    return False


# unit: ( structDef | fnDef | varDef )* END
def unit():
    while True:
        if structDef():
            pass
        elif fnDef():
            pass
        elif varDef():
            pass
        else:
            break
    if consume("END"):
        return True
    return False

def parse(tokensList):
    global tokens
    tokens = tokensList
    if not unit():
        tkerr("syntax error")
