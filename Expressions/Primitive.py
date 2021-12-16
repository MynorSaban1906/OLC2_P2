from Abstract.Instruction import Instruction
from Abstract.NodoAST import NodoAST
from SymbolsTable.Type import Type
from  Abstract.Expression import Expression
from Expressions.Value import Value
from Abstract.Expression import Expression


# solo devuelve el Value del id
class Primitive(Instruction):
    def __init__(self, Type, Value, Row, Column):
        Expression.__init__(self,Row,Column)
        self.Type = Type
        self.Value = Value
        self.Row = Row
        self.Column = Column


    def interpreter(self, tree, table):
        
        if self.getType() in (Type.ENTERO, Type.DECIMAL):
            return Value(self.getValue(), self.getType(), False,self.Value)
        elif self.getType() == Type.BOOLEANO:
            if self.trueLb=='':
                self.trueLb=tree.addLiteral()
            if self.falseLb=='':
                self.falseLb=tree.addLiteral()
            if(self.Value):
                tree.addGoto(self.trueLb)
                tree.addComment("GOTO PARA EVITAR")
                tree.addGoto(self.falseLb)
            else:
                tree.addGoto(self.falseLb)
                tree.addComment("GOTO PARA EVITAR")
                tree.addGoto(self.trueLb)
            ret= Value(self.Value,self.Type,False,self.Value)
            ret.true_label=self.trueLb
            ret.false_label=self.falseLb
            return ret
        elif self.getType()==Type.CADENA:
            tempIn=tree.addTemporal()
            tree.addExp(tempIn,'H','', '')
            for ch in self.Value:
                tree.setHeap(ord(ch),'H')
                tree.addH()
            tree.setHeap(-1,'H')
            tree.addH()
            return Value(tempIn, self.getType(), False,self.Value)
        else:
            return "NO programado"

    def getNodo(self):
        nodo=NodoAST("PRIMITIVE")
        nodo.Agregar_Hijo(str(self.getValue()))
        return nodo
        

    
    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type

    def getValue(self):
        return self.Value

    def setValue(self, Value):
        self.Value = Value

        
    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column