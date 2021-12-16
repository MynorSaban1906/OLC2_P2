from typing import OrderedDict
from Expressions.Value import Value
from SymbolsTable.Type import Type,LogicOperator
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Symbols import Symbols
from Abstract.Instruction import Instruction, Instruction
from Abstract.NodoAST import NodoAST


class Logic(Instruction):
    def __init__(self, Operator, OperacionIzq, OperacionDer, Row, Column):
        self.Operator = Operator
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.Row = Row
        self.Column = Column
        self.Type = Type.BOOLEANO
        self.true_label=''
        self.false_label=''

    # operaciones logicas 
    # se inerpretan cada instruccion segun el Operator en este caso es el simbolo 
    # lo cual debe de generar una respuesta booleana
    def interpreter(self, tree, table):
        self.checkLabels(tree)
        lbAndOr=''

        if self.Operator == LogicOperator.AND:
           lbAndOr=self.OperacionIzq.true_label=tree.addLiteral()    
           self.OperacionDer.true_label=self.true_label
           self.OperacionIzq.false_label= self.OperacionDer.false_label=self.false_label


        elif self.Operator == LogicOperator.OR:
            self.OperacionIzq.true_label=self.OperacionDer.true_label=self.true_label
            lbAndOr= self.OperacionIzq.false_label= tree.addLiteral()
            self.OperacionDer.false_label=self.false_label
        
        izq = self.OperacionIzq.interpreter(tree, table)
        if izq.type!=Type.BOOLEANO:
            print('no se puede men')
            return 
        
        tree.putLabel(lbAndOr)

        der = self.OperacionDer.interpreter(tree, table)
        if der.type!=Type.BOOLEANO:
            print('no se puede')
            return
        if isinstance(der, Exceptions): return der
        
        ret = Value(None,Type.BOOLEANO,False)
        ret.true_label=self.true_label
        ret.false_label= self.false_label
        return ret


    def obtenerVal(self, Type, val):
        if Type == Type.ENTERO:
            return int(val)
        elif Type == Type.DECIMAL:
            return float(val)
        elif Type == Type.BOOLEANO:
            return bool(val)
        return str(val)



    def getNodo(self):
        nodo= NodoAST("EXPRESSION")  
        if self.OperacionDer != None:
            nodo.Agregar_Hijo_Nodo(self.OperacionIzq.getNodo())
            nodo.Agregar_Hijo(self.simb(self.Operator.name))
            nodo.Agregar_Hijo_Nodo(self.OperacionDer.getNodo())
        else:
            nodo.Agregar_Hijo(self.simb(self.Operator.name))
            nodo.Agregar_Hijo_Nodo(self.OperacionIzq.getNodo())
            
            
        return nodo



    def simb(self, Operator):
        if Operator=="NOT":
            return "!"
        elif Operator=="AND":
            return "&&"
        elif Operator=="OR":
            return "||"

    def checkLabels(self,tree):
        if self.true_label=='':
            self.true_label = tree.addLiteral()
        if self.false_label=='':
            self.false_label= tree.addLiteral()


    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column
 
    def getType(self):
        return self.Type

    def setType(self, Type):
        self.Type=Type

 
    def getOperacionIzq(self):
        return self.OperacionIzq

    def setOperacionIzq(self, OperacionIzq):
        self.OperacionIzq=OperacionIzq

    def getOperacionDer(self):
        return self.OperacionDer

    def setOperacionDer(self, OperacionDer):
        self.OperacionDer=OperacionDer
