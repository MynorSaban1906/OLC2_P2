from Expressions.Value import Value
from SymbolsTable.Type import Type, RelationalOperator
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Symbols import Symbols
from Abstract.Instruction import Instruction
from Abstract.NodoAST import NodoAST



class Relational(Instruction):
    def __init__(self, Operator, OperacionIzq, OperacionDer, Row, Column):
        self.Operator = Operator
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.Row = Row
        self.Column = Column
        self.Type = Type.BOOLEANO
        self.false_label=''
        self.true_label=''
        # verifica las instrucciones de cada Operator
        #el . interprete sirve para que ejecute las instrucciones que se adecuen al Type de operacion
        
    
    def interpreter(self, tree, table):
        izq = self.OperacionIzq.interpreter(tree, table)
        if isinstance(izq, Exceptions): return izq
        der =None

        result = Value(None,Type.BOOLEANO,False)

        if izq.type!= Type.BOOLEANO:
            der = self.OperacionDer.interpreter(tree,table)
            if izq.type in (Type.ENTERO, Type.DECIMAL) and der.type in (Type.ENTERO, Type.DECIMAL):
                self.checkLabels(tree)
                tree.addIf(izq.value,der.value,self.simb(self.Operator.name),self.true_label)
                tree.addGoto(self.false_label)

        else:
            gotoRigth=tree.addLiteral()
            leftTemp= tree.addTemporal()

            tree.putLabel(izq.true_label)
            tree.addExp(leftTemp,'1','','')
            tree.addGoto(gotoRigth)
            
            tree.putLabel(izq.false_label)
            tree.addExp(leftTemp,'0','','') 
                 
            tree.putLabel(gotoRigth)

            der= self.OperacionDer.interpreter(tree,table)
            if der.type != Type.BOOLEANO:
                print('no es operable bro')
                return
            gotoEnd= tree.addLiteral()
            rightTemp=tree.addTemporal()


            tree.putLabel(der.true_label)

            tree.addExp(rightTemp,'1','','')
            tree.addGoto(gotoEnd)

            tree.putLabel(der.false_label)
            tree.addExp(rightTemp,'0','','')
        
            tree.putLabel(gotoEnd)
            self.checkLabels(tree)
            tree.addIf(leftTemp,rightTemp,self.simb(self.Operator.name),self.true_label)
            tree.addGoto(self.false_label)
        
        result.true_label= self.true_label
        result.false_label=self.false_label
        return result

            
    def obtenerVal(self, Type, val):
        if Type == Type.ENTERO:
            if type(val) is str:
                return str(val)
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

    def checkLabels(self,tree):
        if self.true_label=='':
            self.true_label = tree.addLiteral()
        if self.false_label=='':
            self.false_label= tree.addLiteral()


    def simb(self, Operator):
        if Operator=="NOT":
            return "!"
        elif Operator=="AND":
            return "&&"
        elif Operator=="OR":
            return "||"
        elif Operator=="MENORQUE":
            return "<"
        elif Operator=="MAYORQUE":
            return ">"
        elif Operator=="MENORIGUAL":
            return "<="
        elif Operator=="MAYORIGUAL":
            return ">="
        elif Operator=="IGUALIGUAL":
            return "=="
        elif Operator=="DIFERENTE":
            return "!="