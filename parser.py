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
        else:
            tkerr("lipseste OR dupa expresia AND")
    iTk = start
    return False

# ExprOrPrim: OR exprAnd ExprOrPrim | ε
def exprOrPrim():
    global iTk
    start = iTk
    if consume("OR"):
        if exprAnd():
            if exprOrPrim():
                return True
        else:
            tkerr("lipseste expresia dupa OR")
    iTk = start
    return True  # epsilon

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
                            tkerr("lipseste expresia dupa ,")
                            break
                    else:
                        break
            if consume("RPAR"):
                return True
            else:
                tkerr("lipseste ) dupa apelul de functie")
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
            else:
                tkerr("lipseste ) dupa expresia din paranteze")
        else:
            tkerr("lipseste expresia din paranteze in expresia primara")
    iTk = start
    return False


# exprUnary: ( SUB | NOT ) exprUnary | exprPostfix
def exprUnary():
    global iTk
    start = iTk
    if consume("SUB"):
        if exprUnary():
            return True
        else:
            tkerr("lipseste expresia dupa -")
    if consume("NOT"):
        if exprUnary():
            return True
        else:
            tkerr("lipseste expresia dupa !")
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
                else:
                    tkerr("lipseste expresia dupa ) in expresia de cast")
            else:
                tkerr("lipseste ) in expresia de cast")
        else:
            tkerr("lipseste tipul in expresia de cast")
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
        else:
            tkerr("lipseste expresia de tip postfix dupa expresia primara")
    iTk = start
    return False

#ExprPostfixPrim: LBRACKET expr RBRACKET ExprPostfixPrim | DOT ID ExprPostfixPrim | ε
def exprPostfixPrim():
    if consume("LBRACKET"):
        if expr():
            if consume("RBRACKET"):
                if exprPostfixPrim():
                    return True
            else:
                tkerr("lipseste ] in expresia de tip postfix")
        else:
            tkerr("lipseste expresia intre [] in expresia de tip postfix")
    if consume("DOT"):
        if consume("ID"):
            if exprPostfixPrim():
                return True
        else:
            tkerr("lipseste numele campului dupa . in expresia de tip postfix")
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
        else:
            tkerr("lipseste MUL|DIV dupa expresia CAST")
    iTk = start
    return False

#ExprMulPrim: ( MUL | DIV ) exprCast ExprMulPrim | ε
def exprMulPrim():
    if consume("MUL") or consume("DIV"):
        if exprCast():
            if exprMulPrim():
                return True
        else:
            tkerr("lipseste expresia dupa MUL|DIV")
    return True


#EprAdd: ExprMul exprAddPrim
def exprAdd():
    global iTk
    start = iTk
    if exprMul():
        if exprAddPrim():
            return True
        else:
            tkerr("lipseste ADD|SUB dupa expresia MUL|DIV")
    iTk = start
    return False

#ExprAddPrim: ( ADD | SUB ) exprMul ExprAddPrim | ε
def exprAddPrim():
    if consume("ADD") or consume("SUB"):
        if exprMul():
            if exprAddPrim():
                return True
        else:
            tkerr("lipseste expresia dupa ADD|SUB")
    return True



#EprRel: ExprAdd exprRelPrim
def exprRel():
    global iTk
    start = iTk
    if exprAdd():
        if exprRelPrim():
            return True
        else:
            tkerr("lipseste LESS|LESSEQ|GREATER|GREATEREQ dupa expresia ADD | SUB")
    iTk = start
    return False

#ExprRelPrim: ( LESS | LESSEQ | GREATER | GREATEREQ ) exprAdd ExprRelPrim | ε
def exprRelPrim():
    if consume("LESS") or consume("LESSEQ") or consume("GREATER") or consume("GREATEREQ"):
        if exprAdd():
            if exprRelPrim():
                return True
        else:
            tkerr("lipseste expresia dupa LESS|LESSEQ|GREATER|GREATEREQ")
    return True


#EprEq: ExprRel exprEqPrim
def exprEq():
    global iTk
    start = iTk
    if exprRel():
        if exprEqPrim():
            return True
        else:
            tkerr("lipseste EQUAL|NOT EQUAL dupa expresia RELATIONAL")
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
        else:
            tkerr("lipseste expresia dupa EQUAL")
    if consume("NOTEQ"):
        if exprRel():
            if exprEqPrim():
                return True
        else:
            tkerr("lipseste expresia dupa NOT EQUAL")
    iTk = start
    return True

#EprAnd: ExprEq exprAndPrim
def exprAnd():
    global iTk
    start = iTk
    if exprEq():
        if exprAndPrim():
            return True
        else:
            tkerr("lipseste AND dupa expresia EQUAL | NOT EQUAL")
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
        else:
            tkerr("lipseste expresia dupa AND")
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
        else:
            tkerr("lipseste ] dupa declararea vectorului")
    iTk = start
    return False

# fnDef: ( typeBase | VOID ) ID LPAR ( fnParam ( COMMA fnParam )* )? RPAR stmCompound
def fnDef():
    global iTk
    start = iTk
    if typeBase() or consume("VOID"):
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
                                tkerr("parametru functiei invalid sau lipseste dupa ,")
                                break # eroare
                        else:
                            break # eroare
                if consume("RPAR"):
                    if stmCompound():
                        return True
                    else:
                        tkerr("lipseste corpul functiei")
                else:
                    tkerr("lipseste ) dupa declararea functiei")
            else:
                tkerr("lipseste ( dupa numele functiei")
        else:
            tkerr("lipseste numele functiei")
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
        else:
            tkerr("lipseste numele parametrului")
    iTk = start
    return False

# stm: stmCompound | IF LPAR expr RPAR stm ( ELSE stm )? | WHILE LPAR expr RPAR stm | RETURN expr? SEMICOLON | expr? SEMICOLON
def stm(needStmCompound = False):
    global iTk
    start = iTk
    if stmCompound():
        return True
    elif needStmCompound:
        tkerr("corpul necesar functiei lipseste sau este incorect")
    if consume("IF"):
        if consume("LPAR"):
            if expr():
                if consume("RPAR"):
                    if stm():
                        if consume("ELSE"):
                            if stm():
                                pass
                            else:
                                tkerr("lipseste corpul else-ului")
                        return True
                    else:
                        tkerr("lipseste corpul if-ului")
                else:
                    tkerr("lipseste ) dupa conditia if-ului")
            else:
                tkerr("conditia if-ului lipseste sau nu este corecta")
        else:
            tkerr("lipseste ( dupa if")

    if consume("WHILE"):
        if consume("LPAR"):
            if expr():
                if consume("RPAR"):
                    if stm(True):
                        return True
                    else:
                        tkerr("lipseste sau e definit incorect corpul while-ului")
                else:
                    tkerr("lipseste ) dupa conditia while-ului")
            else:
                tkerr("conditia while-ului lipseste sau nu este corecta")
        else:
            tkerr("lipseste ( dupa while")
    if consume("RETURN"):
        if expr():
            pass
        if consume("SEMICOLON"):
            return True
        else:
            tkerr("lipseste ; de la return sau expresia returnata este invalida")
    if expr():
        if consume("SEMICOLON"):
            return True
        else:
            tkerr("lipseste ; dupa expresie")
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
        else:
            tkerr("lipseste } dupa corpul functiei sau stuctura ori definitie invalida")
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
            else:
                tkerr("lipseste expresia dupa =")
    iTk = start
    if exprOr():
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
