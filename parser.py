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
                    else:
                        tkerr("lipseste ; dupa } in definitia de structura")
                else:
                    tkerr("lipseste } in definitia de structura")
            else:
                tkerr("lipseste { in definitia de structura")
        else:
            tkerr("lipseste numele structurii")
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

#EprPostfix: ExprPrimary exprPostfixPrim
def exprPostfix():
    global iTk
    start = iTk
    if exprPrimary():
        if exprPostfixPrim():
            return True
    iTk = start
    return False

#ExprPostfixPrim: LBRACKET expr RBRACKET ExprPostfixPrim | DOT ID ExprPostfixPrim | ε
def exprPostfixPrim():
    if consume("LBRACKET"):
        if expr():
            if consume("RBRACKET"):
                if exprPostfixPrim():
                    return True
    if consume("DOT"):
        if consume("ID"):
            if exprPostfixPrim():
                return True
    return True


#exprUnary: ( SUB | NOT ) exprUnary | exprPostfix
def exprUnary():
    global iTk
    start = iTk
    if consume("SUB") or consume("NOT"):
        if exprUnary():
            return True
    if exprPostfix():
        return True
    iTk = start
    return False

#ExprUnaryPrim: ( SUB | NOT ) exprUnary ExprUnaryPrim | ε
def exprUnaryPrim():
    if consume("SUB") or consume("NOT"):
        if exprUnary():
            if exprUnaryPrim():
                return True
    return True


#EprMul: ExprCast exprMulPrim
def exprMul():
    global iTk
    start = iTk
    if exprCast():
        if exprMulPrim():
            return True
    iTk = start
    return False

#ExprMulPrim: ( MUL | DIV ) exprCast ExprMulPrim | ε
def exprMulPrim():
    if consume("MUL") or consume("DIV"):
        if exprCast():
            if exprMulPrim():
                return True
    return True


#EprAdd: ExprMul exprAddPrim
def exprAdd():
    global iTk
    start = iTk
    if exprMul():
        if exprAddPrim():
            return True
    iTk = start
    return False

#ExprAddPrim: ( ADD | SUB ) exprMul ExprAddPrim | ε
def exprAddPrim():
    if consume("ADD") or consume("SUB"):
        if exprMul():
            if exprAddPrim():
                return True
    return True



#EprRel: ExprAdd exprRelPrim
def exprRel():
    global iTk
    start = iTk
    if exprAdd():
        if exprRelPrim():
            return True
    iTk = start
    return False

#ExprRelPrim: ( LESS | LESSEQ | GREATER | GREATEREQ ) exprAdd ExprRelPrim | ε
def exprRelPrim():
    if consume("LESS") or consume("LESSEQ") or consume("GREATER") or consume("GREATEREQ"):
        if exprAdd():
            if exprRelPrim():
                return True
    return True


#EprEq: ExprRel exprEqPrim
def exprEq():
    global iTk
    start = iTk
    if exprRel():
        if exprEqPrim():
            return True
    iTk = start
    return False

# exprEqPrim: ( EQUAL | NOTEQ ) exprRel exprEqPrim | ε
def exprEqPrim():
    global iTk
    start = iTk
    if consume("EQUAL"):
        if exprRel():
            if exprEqPrim():
                return True
    if consume("NOTEQ"):
        if exprRel():
            if exprEqPrim():
                return True
    iTk = start
    return True

#EprAnd: ExprEq exprAndPrim
def exprAnd():
    global iTk
    start = iTk
    if exprEq():
        if exprAndPrim():
            return True
    iTk = start
    return False

#ExprAndPrim: AND exprEq ExprAndPrim | ε
def exprAndPrim():
    global iTk
    start = iTk
    if consume("AND"):
        if exprEq():
            if exprAndPrim():
                return True
    iTk = start
    return True  # epsilon

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
            else:
                tkerr("lipseste ; dupa declararea variabilei")
        else:
            tkerr("lipseste numele variabilei")
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
    # else:
        # tkerr("lipseste tipul de return al functiei") # de verificat daca e corecta
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
    else:
        tkerr("programul inexistent")
    return False

def parse(tokensList):
    global tokens
    tokens = tokensList
    if not unit():
        tkerr("syntax error")
