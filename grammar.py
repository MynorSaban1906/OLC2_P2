#  gramatica implementada para analizador de lenguaje julia

from Expressions.Id import Id
from Instruction.Break import Break
from Instruction.Continue import Continue
from Instruction.LlamadaFuncion import LlamadaFuncion
from Instruction.Return import Return

from Instruction.Statement import Statement
from Natives.Float import Float
from Natives.Lowercase import Lowercase
from Natives.Parse import Parse
from Natives.String import String
from Natives.Trunc import Trunc
from Natives.Uppercase import Uppercase
from SymbolsTable.Type import ArithmeticOperator, LogicOperator
from Expressions.Aritmetic import Aritmetic
from SymbolsTable.Exceptions import Exceptions
from Expressions.Primitive import Primitive
from SymbolsTable.Type import Type,RelationalOperator
from Instruction.Print import Print
from Expressions.Relational import Relational
from Expressions.Logic import Logic
from Instruction.If import If
from Instruction.InstStatement import InstStatement
from Instruction.While import While
from Instruction.For import For



import sys

sys.getrecursionlimit()
sys.setrecursionlimit(4000)


import os
import re

errores = [] # array de errores que se registro en el codigo

reservadas = {
    'pop'       : 'RPOP',
    'push'      : 'RPUSH',
    'print'     : 'PRINT',
    'println'   : 'PRINTLN',
    'true'      : 'RTRUE',
    'false'     : 'RFALSE',
    'null'      : 'NULO',
    'Int64'     : 'RINT',
    'Float64'   : 'RDOUBLE',
    'Bool'      : 'RBOLEANO',
    'Char'      : 'RCHAR',
    'string'    : 'RSTRING',
    'end'       : 'END',
    'if'        : 'RIF',
    'else'      : 'RELSE',
    'elseif'    : 'RELSEIF',
    'function'  : 'RFUNCION',
    'return'    : 'RRETURN',
    'parse'     : 'RPARSE',
    'trunc'     : 'RTRUNC',
    'while'     : 'RWHILE',
    'continue'  : 'RCONTINUE',
    'break'     : 'RBREAK',
    'log10'     : 'RLOG10',
    'log'       : 'RLOG',
    'for'       : 'RFOR',
    'in'        : 'RIN',
    'struct'    : 'RSTRUCT',
    'mutable'   : 'RMUTABLE',
    'global'    : 'RGLOBAL',
    'local'     : 'RLOCAL',
    'float'     : 'FLOATPARAM',
    'lowercase' : 'RLOWERCASE',
    'uppercase' : 'RUPPERCASE',
    
}
    # simbolos que se usan en el analizador de julia
tokens  = [
    'PTCOMA',
    'PARIZQ',
    'PARDER',
    'MAS',
    'IGUAL',
    'MENOS',
    'POR',
    'POW',
    'DIVIDIDO',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CHAR',
    'ID',
    'MENQUE',
    'MAYQUE',
    'MODULO',
    'MENIGUAL',
    'MAYIGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'NOT',
    'AND',
    'OR',
    'DPUNTOS',
    'COMA',
    'PUNTOS',
    'CORDER',
    'CORIZQ',
    


] + list(reservadas.values())



# Tokens declarados
t_PTCOMA    = r';'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_IGUAL     = r'='
t_POW       =r'\^'
t_MODULO    =r'\%'

t_MENQUE    =r'<'
t_MAYQUE    =r'>'
t_IGUALIGUAL =r'=='
t_MENIGUAL  =r'<='
t_MAYIGUAL  =r'>='
t_DIFERENTE =r'!='
t_OR        =r'\|\|'
t_AND       =r'&&'
t_NOT       =r'!'
t_DPUNTOS   =r'::'
t_COMA      =r','
t_PUNTOS    =r':'
t_CORDER='\]'
t_CORIZQ='\['



 
def t_DECIMAL(t):
    r'\d+\.\d+'  # expresion regualar
    try:
        t.value = float(t.value)

    except ValueError:
        print("float demasiado grande %d", t.value)
        t.value = 0
    return t


def t_CHAR(t):
    r'(\'([a-zA-Z]|\\\'|\\"|\\t|\\n|\\\\|.)\')' # expresion regualar

    t.value = t.value[1:-1] # remuevo las comillas simples
    return t


def t_ENTERO(t): 
    r'\d+'  # expresion regualar

    try:
        t.value = int(t.value)
    except ValueError:
        print("entero demasiado grande %d", t.value)
        t.value = 0
    return t


def t_CADENA(t):
    r'\"(\"|.)*?\"' # expresion regualar
    t.value = t.value[1:-1] # remuevo las comillas dobles
    return t

# Comentario de multiples lineas #=  ............................ =#

def t_COMENTARIO_MULTILINEA(t):
    r'\#\=(.|\n)*?\=\#'
    t.lexer.lineno += t.value.count('\n')


# Comentario simple # ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"
def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t
 
def t_error(t):
    errores.append(Exceptions("Lexico","El caracter \"" + t.value[0]+"\" no pertenece al lenguaje" , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()



#Precedencia   solo estan las basicas
precedence = (

    ('left','OR'),
    ('left','AND'),
    ('left','IGUALIGUAL','DIFERENTE'),
    ('left', 'MENQUE', 'MAYQUE','MENIGUAL', 'MAYIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO','MODULO'),
    ('left','POW'),
    

)
#Abstract

def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_instrucciones_instruccion(t) :
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
    
# INSTRUCCIONES

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

# INSTRUCCION

def p_instruccion(t) :
    '''instruccion      :   imprimir_instr final  
                        |   declaracion final
                        |   if_instr END final
                        |   while_instr END final
                        |   break_instr final
                        |   continue_instr final
                        |   for_instr END final
                        |   llamadaFuncion final
    '''
    t[0] = t[1]


def p_finins(t) :
    '''final      : PTCOMA
                    | '''
    t[0] = None



def p_instruccion_error(t):
    '''instruccion      : error final'''
    errores.append(Exceptions("Sintactico","Error Sintactico con " + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""

# EXPRESIONES OPERATORIAS


def p_expresiones_operatorias(t):
    '''expresion :      expresion MAS expresion
                    |   expresion MENOS expresion  
                    |   expresion POR expresion  
                    |   expresion DIVIDIDO expresion
                    |   expresion MODULO expresion 
                    |   expresion POW expresion  
                    

                    |   expresion MENQUE expresion  
                    |   expresion MAYQUE expresion  
                    |   expresion MENIGUAL expresion  
                    |   expresion MAYIGUAL expresion 
                    |   expresion DIFERENTE expresion  
                    |   expresion IGUALIGUAL expresion  

                    |   expresion OR expresion  
                    |   expresion AND expresion  
                      
    '''


    if t[2] == '+':   t[0] = Aritmetic(ArithmeticOperator.MAS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':   t[0] = Aritmetic(ArithmeticOperator.MENOS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':   t[0] = Aritmetic(ArithmeticOperator.POR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/':   t[0] = Aritmetic(ArithmeticOperator.DIV, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%':   t[0] = Aritmetic(ArithmeticOperator.MOD, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '^':   t[0] = Aritmetic(ArithmeticOperator.POT, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))


    elif t[2] == '<':   t[0] = Relational(RelationalOperator.MENORQUE , t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':   t[0] = Relational(RelationalOperator.MAYORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':   t[0] = Relational(RelationalOperator.MENORIGUAL , t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':   t[0] =Relational(RelationalOperator.MAYORIGUAL , t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '!=':   t[0] =Relational(RelationalOperator.DIFERENTE , t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '==':   t[0] =Relational(RelationalOperator.IGUALIGUAL , t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))

    elif t[2] == '||':   t[0] = Logic(LogicOperator.OR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&':   t[0] = Logic(LogicOperator.AND, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))

    
# EXPRESIONES PRIMITIVAS
def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0]=t[2]
        

# EXPRESIONES DE EXPRESIONES
def p_primitivo_decimal(t):
    'expresion : DECIMAL'
    t[0] = Primitive(Type.DECIMAL, t[1], t.lineno(1), find_column(input, t.slice[1]))


def p_expresion_entero(t):
    'expresion : ENTERO'
    t[0] = Primitive(Type.ENTERO ,t[1], t.lineno(1), find_column(input, t.slice[1]))


def p_primitivo_cadena(t):
    'expresion : CADENA'
    t[1]=str(t[1]).replace('\\t','\t')
    t[1]=str(t[1]).replace('\\n','\n')
    t[1]=str(t[1]).replace('\\\\','\\')
    t[1]=str(t[1]).replace("\\'","\'")
    t[1]=str(t[1]).replace('\\"','"')
    t[0] = Primitive(Type.CADENA,str(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_char(t):
    'expresion : CHAR'
    t[1]=str(t[1]).replace('\\t','\t')
    t[1]=str(t[1]).replace('\\n','\n')
    t[1]=str(t[1]).replace('\\\\','\\')
    t[1]=str(t[1]).replace("\\'","\'")
    t[1]=str(t[1]).replace('\\"','"')
    t[0] = Primitive(Type.CHARACTER,str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_nulo(t):
    'expresion : NULO'
    t[0] = Primitive(Type.NULO,None, t.lineno(1), find_column(input, t.slice[1]))
def p_primitivo_true(t):
    '''expresion : RTRUE'''
    t[0] = Primitive(Type.BOOLEANO, True, t.lineno(1), find_column(input, t.slice[1]))

def p_primitivo_false(t):
    '''expresion : RFALSE'''
    t[0] = Primitive(Type.BOOLEANO, False, t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_id(t):
    'expresion : ID'
    t[0] = Id(t[1], t.lineno(1), find_column(input, t.slice[1]))


def p_expresion_llamada(t):
    'expresion :    llamadaFuncion    '
    t[0]=t[1]
#

def p_expresionLista(t):
    '''
        expresionlist : expresionlist COMA expresion
                    |   expresion
    '''
    if len(t)==2:
        t[0]=[t[1]]
    else:
        t[1].append(t[3])
        t[0]= t[1]


#   IMPRIMIR

def p_imprimir(t) :
    '''imprimir_instr   :   PRINT PARIZQ expresionlist PARDER
                        |   PRINTLN PARIZQ expresionlist PARDER    '''
                        
    if t[1]=="print": t[0] = Print(t[3], t.lineno(1), find_column(input, t.slice[1]))
    if t[1]=="println": t[0] = Print(t[3], t.lineno(1), find_column(input, t.slice[1]),True)

# DECLARACION

def p_declaracion_jocl(t):
    '''
        declaracion :   declaracion1
                    |   declaracion2
    '''
    t[0]=t[1]

def p_declaracion_jocl1(t):
    '''
        declaracion1 :   ID IGUAL expresion
    '''
    t[0]=Statement(t[1], t.lineno(1), find_column(input, t.slice[1]),t[3],None)

def p_declaracion_jocl2(t):
    '''
     declaracion2 :  ID IGUAL expresion DPUNTOS tipo
    '''
    t[0]=Statement(t[1], t.lineno(1), find_column(input, t.slice[1]),t[3],t[5])

# string, array  es un heap porque este va variando durante el tiempo
# int, float es para un stack ya que este ocupa todo el espacio y no cambia su tama;o en ejecucion

# TIPO 
def p_tipo(t) :
    '''tipo     : ID
                '''
    if t[1] == 'Int64':
        t[0] = Type.ENTERO
    elif t[1] == 'Float64':
        t[0] = Type.DECIMAL
    elif t[1] == 'String':
        t[0] = Type.CADENA
    elif t[1] == 'Bool':
        t[0] = Type.BOOLEANO
    elif t[1] == 'Char':
        t[0] = Type.CHARACTER
    elif t[1] == 'Null':
        t[0] = Type.NULO

# STATEMENT
def p_statement2(t):
    '''statement : instrucciones'''
    t[0] = InstStatement(t[1], t.lineno(0), t.lexpos(0))

# IF 

def p_if1(t) :
    'if_instr     : RIF expresion statement '
    t[0] = If(t[2], t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_if2(t) :
    'if_instr     : RIF expresion statement RELSE statement'
    t[0] = If(t[2], t[3], t.lineno(1), find_column(input, t.slice[1]),t[5])

def p_if3(t) :
    'if_instr     : RIF expresion statement  elseIfList'
    t[0] = If(t[2], t[3], t.lineno(1), find_column(input, t.slice[1]),t[4])

def p_if4(t):
    '''elseIfList   : RELSEIF expresion statement
                    | RELSEIF expresion statement RELSE statement
                    | RELSEIF expresion statement  elseIfList'''
    if len(t) == 4:
        t[0] = If(t[2], t[3], t.lineno(1), find_column(input, t.slice[1]))
    elif len(t) == 6:
        t[0] = If(t[2], t[3], t.lineno(1), find_column(input, t.slice[1]), t[5])
    elif len(t) == 5:
        t[0] = If(t[2], t[3], t.lineno(1), find_column(input, t.slice[1]), t[4])



# while

def p_while(t) :
    'while_instr     : RWHILE expresion instrucciones '
    t[0] = While(t[2], t[3], t.lineno(1), find_column(input, t.slice[1]))



# BREAK
def p_break(t) :
    'break_instr     : RBREAK'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))

# CONTINUE
def p_continue(t) :
    'continue_instr     : RCONTINUE'
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))



def p_cicloFor(t):
    '''
        for_instr :     RFOR ID RIN expresion PUNTOS expresion instrucciones
                    |   RFOR ID RIN expresion instrucciones
                    |   RFOR ID RIN CORIZQ expresiones_array CORDER instrucciones 
    '''
    if len(t)==6:
        t[0]= For(t[2],t[4], t[5],t.lineno(1), find_column(input, t.slice[1]),None)

    elif t[4]=='[':
        t[0]= For(t[2],t[5], t[7],t.lineno(1), find_column(input, t.slice[1]),None)
    else:
        t[0]= For(t[2],t[4],t[7], t.lineno(1), find_column(input, t.slice[1]),t[6])


# lista de dimensiones 
def p_array1(t):
    '''    
    expresiones_array : expresiones_array COMA ex
                    |   ex
    
    '''
    if len(t)==2:
        t[0]=[t[1]]
    else:
        t[1].append(t[3])
        t[0]=t[1]

def p_array2(t):
    '''ex : CORIZQ expresiones_array CORDER 
                | expresion
    
    '''
    if len(t)==2:
        t[0]=t[1]
    else:
        t[0]=t[2]

 #   FUNCIONES NATIVAS 

def p_trunc(t):
    '''expresion  :   RTRUNC PARIZQ expresion PARDER '''
    t[0]= Trunc(t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_rstring(t):
    '''expresion  :   RSTRING PARIZQ expresion PARDER '''
    t[0]=String(t[3], t.lineno(1), find_column(input, t.slice[1]))


def p_rlowercase(t):
    '''expresion  :   RLOWERCASE PARIZQ expresion PARDER '''
    t[0]=Lowercase(t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_rlowercase(t):
    '''expresion  :   RUPPERCASE PARIZQ expresion PARDER '''
    t[0]=Uppercase(t[3], t.lineno(1), find_column(input, t.slice[1]))




def p_floatpara(t):
    '''expresion  :   FLOATPARAM PARIZQ expresion PARDER '''
    t[0]=Float(t[3], t.lineno(1), find_column(input, t.slice[1]))



def p_parseval(t):
    '''expresion  :   RPARSE PARIZQ ID  COMA expresion PARDER '''
    t[0]= Parse(t[3],t[5], t.lineno(1), find_column(input, t.slice[1]))



def p_llamadaFuncionParametro (t):
    'llamadaFuncion  : ID PARIZQ parametros_llamada PARDER '
    t[0] = LlamadaFuncion(t[1], t[3],t.lineno(2), find_column(input, t.slice[2]))

# PARAMETROS LLAMADA A FUNCION

def p_parametrosLL_1(t) :
    'parametros_llamada     : parametros_llamada COMA parametro_llamada'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_parametrosLL_2(t) :
    'parametros_llamada    : parametro_llamada'
    t[0] = [t[1]]



# PARAMETRO LLAMADA A FUNCION

def p_parametroLL(t) :
    'parametro_llamada     : expresion'
    t[0] = t[1]




import ply.yacc as yacc
parser = yacc.yacc()
input = ''

def parse(inp) :
    global errores
    global lexer
    global parser 
    errores = []
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)

from SymbolsTable.Table import Table
from SymbolsTable.Tree import Tree

archivo=open("entrega.jl","r")
entrada=archivo.read()
instrucciones = parse(entrada) #ARBOL AST
Arbol_cst = Tree(instrucciones)
TablaSimboloGlobal = Table(entorno="GLOBAL",declaracionTipo="variable",Row=0,Column=0)
Arbol_cst.setTablaSimboloGlobal(TablaSimboloGlobal)
 # se crean las funciones nativas


# se crean las funciones nativa
for error in errores:                   #CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
    Arbol_cst.getExcepciones().append(error)
for instruccion in Arbol_cst.getInstrucciones():
        value = instruccion.interpreter(Arbol_cst,TablaSimboloGlobal)
        if isinstance(value,Exceptions):
            Arbol_cst.getExcepciones().append(value)


print("----------errores ------------")
for x in Arbol_cst.getExcepciones():
    print(x.toString())
    

print("----------salida ------------")

print(Arbol_cst.getCode())

ar = open("./misalida.go",'w+')

ar.write(Arbol_cst.getCode())
ar.close()

