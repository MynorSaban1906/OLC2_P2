from Abstract.Instruction import Instruction
from Abstract.NodoAST import NodoAST

class Continue(Instruction):
    def __init__(self, Row, Column):
        self.Row = Row
        self.Column = Column

    def interpreter(self, tree, table):
        if table.continuelb== '':
            print("break fuera de ciclo")
            return self
        tree.addGoto(table.continuelb)
        return self
    def getNodo(self):
        nodo=NodoAST("CONTINUE")
        return nodo

    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column
