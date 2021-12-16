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

class InstStatement(Instruction):
    def __init__(self, id, Row, Column):
        self.instrucciones= id
        self.Row = Row
        self.Column = Column
        


    def interpreter(self, tree, table):
        # esto es para poder guardar el puntero 
        for ins in self.instrucciones:
            ret= ins.interpreter(tree,table)
            if isinstance(ret,Exceptions): return ret
            if ret != None:
                return ret
        

    def getNodo(self):
        nodo=NodoAST("Return")


        return nodo
