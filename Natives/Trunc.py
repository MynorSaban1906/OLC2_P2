from Expressions.Value import Value
from SymbolsTable.Type import Type
from Abstract.Instruction import Instruction
from SymbolsTable.Exceptions import Exceptions
import math
from Abstract.NodoAST import NodoAST


class Trunc(Instruction):
    def __init__(self, expresion, Row, Column):
        self.expresion = expresion
        self.Row = Row
        self.Column = Column
        self.Type = Type

    def interpreter(self, tree, table):

        self.setType(Type.ENTERO) # se cambia a entero por defecto del truncate sin afectar el valor en stack

        value= self.expresion.interpreter(tree,table)  # se interpreta la expresion

        # se devuelve el value , tambien se castea para que se retorne el valor truncado
        return Value(int(value.value),self.Type,False)





    def getNodo(self):
        nodo=NodoAST("TRUNC")
        nodo.Agregar_Hijo_Nodo(self.expresion.getNodo())

        return nodo


    def getId(self):
        return self.Id

    def setId(self, Id):
        self.Id=Id

    
    def getExpresion(self):
        return self.expresion

    def setExpresion(self, expresion):
        self.expresion=expresion

    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type

        
    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column