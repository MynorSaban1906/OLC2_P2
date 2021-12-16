from Expressions.Value import Value
from SymbolsTable.Type import Type
from Abstract.Instruction import Instruction
from SymbolsTable.Exceptions import Exceptions
import math
from Abstract.NodoAST import NodoAST


class Lowercase(Instruction):
    def __init__(self, expresion, Row, Column):
        self.expresion = expresion
        self.Row = Row
        self.Column = Column
        self.Type = None


    def interpreter(self, tree, table):

        simbolo = self.expresion.interpreter(tree,table)
        
        tree.flowercase()
        paramTemp = tree.addTemporal()  
        tree.addExp(paramTemp,'P',table.size,'+')

        tree.newEnv(table.size)

        tree.callFun('lowercase')
        tem=tree.addTemporal()
        tree.getStack('P',tem)
        tree.retEnv(table.size)

        return Value(tem,Type.CADENA,True)# se devuelve el valor en solo mayusculas



    def getNodo(self):
        nodo=NodoAST("LOWERCASE")
        nodo.Agregar_Hijo_Nodo(self.expresion.getNodo())

        return nodo

    def getIdentificador(self):
        return self.identificador

    def setIdentificador(self, identificador):
        self.identificador=identificador

    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type

    def getParametros(self):
        return self.parametros

    def setParametros(self, parametros):
        self.parametros=parametros

    def getInstrucciones(self):
        return self.instrucciones

    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones

        
    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column