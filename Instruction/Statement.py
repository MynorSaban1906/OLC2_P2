
from Expressions.Value import Value
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Type import Type
from Abstract.Instruction import Instruction
from SymbolsTable.Symbols import Symbols
from SymbolsTable.Table import Table
from SymbolsTable.Exceptions import Exceptions
from Instruction.Assignment import Assignment
import copy
from Abstract.NodoAST import NodoAST




class Statement(Instruction):
    def __init__(self, id, Row, Column, Expression=0, Type=None):
        self.id = id
        self.Type = Type
        self.Expression = Expression
        self.Row = Row
        self.Column = Column
        self.arreglo = False
        self.true_label=''
        self.false_label=''
        


    def interpreter(self, tree, table):
        # esto es para poder guardar el puntero 

        
        
        value = self.Expression.interpreter(tree, table) # Valor a asignar a la variable

        if isinstance(value, Exceptions): return value

        if table.SearchAux(self.id):
            retorno= table.getTabla(self.id)
            nuevoValor=Symbols(self.id,retorno.type,self.Row,self.Column,value.value,retorno.puntero,retorno.isGlobal,retorno.inHeap,retorno.result)
            result = table.updateTable(nuevoValor)
            if isinstance(result,Exceptions): return result
            tree.setStack(retorno.puntero,value.value)
            return None
        # guardo la variable en la tabla de simbolos(self, symbolID, symbolType, position, globalVar, inHeap, structType = ""):

        result = table.setTabla(self.id, self.Expression.Type , self.Row, self.Column, value.value,(value.type == Type.CADENA or value.type==Type.NULO),value.result,table)
        
        if isinstance(result, Exceptions): return result

        result = table.getTabla(self.id)
        puntero = result.puntero
        if (result.isGlobal):
            temppos= tree.addTemporal()
            tree.addExp(temppos,'P',result.puntero,"+")

        if result.type ==  Type.BOOLEANO:
            temLb = tree.addLiteral()

            tree.putLabel(value.true_label)
            tree.setStack(result.puntero,"1")

            tree.addGoto(temLb)

            tree.putLabel(value.false_label)
            tree.setStack(result.puntero,"0")
            tree.putLabel(temLb)
            self.setType(result.getType()) 
            return None
                            
        

        self.setType(result.getType())  # AUN ESTA EN PRUEBA

        tree.setStack(puntero,value.value)


        return None
        
        
    def VerificType(self,string):
        if string=="Int64":
            return Type.ENTERO
        elif string=="Float64":
            return Type.DECIMAL
        elif string=="Char":
            return Type.CHARACTER
        elif string=="String":
            return Type.CADENA
        elif string=="bool":
            return Type.BOOLEANO
        elif string=="None":
            return Type.NULO
        else:
            return Type.ID


    def getNodo(self):
        nodo=NodoAST("ASIGNACION")
        nodo.Agregar_Hijo(str(self.getid()))
        nodo.Agregar_Hijo("=")
        nodo.Agregar_Hijo_Nodo(self.getExpression().getNodo())
        return nodo
        


    def getid(self):
        return self.id

    def setid(self, id):
        self.id=id

        
    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type

    def getExpression(self):
        return self.Expression

    def setExpression(self,Expression):
        self.Expression= Expression

    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column
