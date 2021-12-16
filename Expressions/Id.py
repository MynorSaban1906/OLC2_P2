from Expressions.Value import Value
from SymbolsTable.Type import Type
from SymbolsTable.Symbols import Symbols
from Abstract.Instruction import Instruction
from SymbolsTable.Exceptions import Exceptions
from Abstract.NodoAST import NodoAST
from Abstract.Expression import Expression

class Id(Instruction):

# identifica que que Type y obtiene el valor de ella 
# aqui se verifica si ya existe y si no lo guarda la variable
    def __init__(self, Id, Row, Column):
        self.Id = Id
        self.Row = Row
        self.Column = Column
        self.Type = None
        self.true_label = ''
        self.false_label = ''
        self.structType = ''
        
    def interpreter(self, tree, table):
        simbolo = table.getTabla(self.Id)
        
        if simbolo == None:
            return Exceptions("Semantico", "Variable " + self.Id + " no encontrada.", self.Row, self.Column)
        
        tree.addComment("compilacion de accesso")

        self.Type = simbolo.getType()

        temp = tree.addTemporal()
        
        temPos = simbolo.puntero


        tree.getStack( temPos,temp)

        if simbolo.type != Type.BOOLEANO:
            tree.addComment("FIN COMPILACION ACCESO")
            
            return Value(temp, simbolo.type,True,simbolo.value)
        if self.true_label == '':
            self.true_label= tree.addLiteral()
        if self.false_label=='':
            self.false_label= tree.addLiteral()

        tree.addIf(temp,'1' , '==',self.true_label)
        tree.addGoto(self.false_label)

        tree.addComment("FIN COMPILACION ACCESO")
        
        ret = Value(None,Type.BOOLEANO,False,simbolo.value)
        ret.true_label=self.true_label
        ret.false_label=self.false_label
        return ret
        
    def getNodo(self):
        nodo=NodoAST("ID")
        nodo.Agregar_Hijo(str(self.getId()))
        return nodo
        



    def getId(self):
        return self.Id

    def setId(self, Id):
        self.Id=Id

        
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
