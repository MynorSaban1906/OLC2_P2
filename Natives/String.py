from SymbolsTable.Type import Type
from Instruction.Function import Function
from SymbolsTable.Exceptions import Exceptions
from Abstract.NodoAST import NodoAST
from Expressions.Value import Value
from Abstract.Instruction import Instruction

class String(Instruction):
    def __init__(self, expresion, Row, Column):
        self.expresion = expresion
        self.Row = Row
        self.Column = Column
        self.Type = Type

    def interpreter(self, tree, table):

        simbolo= self.expresion.interpreter(tree,table)

        if simbolo ==None:
            return Exceptions("Semantico", "No se encontro el parametro de STRING", self.getRow(),self.getColumn())

        self.setType(Type.CADENA)
        
        ret_tem= tree.addTemporal()
        tree.addExp(ret_tem,'H','','')

        for char in str(simbolo.result):
            tree.setHeap(ord(char),'H')
            tree.addH()

        tree.setHeap('-1','H')
        tree.addH()

        return Value(ret_tem,self.Type,True)
        


    def getNodo(self):
        nodo=NodoAST("STRING")
        nodo.Agregar_Hijo_Nodo(self.expresion.getNodo())

        return nodo

    def getId(self):
        return self.Id

    def setId(self, Id):
        self.Id=Id

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