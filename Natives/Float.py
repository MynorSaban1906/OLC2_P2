from Expressions.Value import Value
from SymbolsTable.Type import Type
from Instruction.Function import Function
from SymbolsTable.Exceptions import Exceptions
import math
from Abstract.NodoAST import NodoAST
from Abstract.Instruction import Instruction

class Float(Instruction):
    def __init__(self, expresion, Row, Column):
        self.expresion = expresion
        self.Row = Row
        self.Column = Column
        self.Type = Type

    def interpreter(self, tree, table):
        simbolo = self.expresion.interpreter(tree,table)
        if simbolo ==None:
            return Exceptions("Semantico", "No se encontro el parametro de Float ", self.getRow(),self.getColumn())

        if simbolo.type not in(Type.ENTERO, Type.DECIMAL): # si no es igual al Type entero o decimal este entraria en un error
            return Exceptions("Semantico", "No se puede usar Float  "  , simbolo.getRow(),simbolo.getColumn())
     
      
        self.setType(Type.DECIMAL) # se pasa el Type de dato el cual siempre seria Type cadena
        
        return Value(float(simbolo.value),self.Type,False)# se devuelve el valor ya tuncado por la funcion math.trunc 
            
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