from SymbolsTable.Type import Type, ArithmeticOperator
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Symbols import Symbols
from Abstract.Instruction import Instruction
from Abstract.NodoAST import NodoAST


from General import General
from Expressions.Value import Value
class Aritmetic(Instruction):

    def __init__(self, Operator, OperacionIzq, OperacionDer, Row, Column):
        self.Operator = Operator
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.Row = Row
        self.Column = Column
        self.Type = None  
        

    def interpreter(self, tree, table):
        # verifica las instrucciones de cada Operator
        #el interprete sirve para que ejecute las instrucciones que se adecuen al Type de operacion
        izq = self.OperacionIzq.interpreter(tree, table)
        if isinstance(izq, Exceptions): return izq
        # sirve por si viene un unario o solo una operacion 
        if self.OperacionDer != None:
            der = self.OperacionDer.interpreter(tree, table)
            if isinstance(der, Exceptions): return der

        # aqui se verifica el Type de operaciones aritmeticas que se realizar 


        if self.Operator == ArithmeticOperator.MAS: #SUMA
            # OPERACION SOLO DE ENTEROS
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.ENTERO
                temp= tree.addTemporal()
                operation=self.simb(self.Operator.name)
                tree.addExp(temp,izq.value,der.value,operation)
                return Value(temp,Type.ENTERO,True)

            elif self.OperacionIzq.Type in (Type.ENTERO,Type.DECIMAL) and self.OperacionDer.Type in (Type.ENTERO,Type.DECIMAL):
                self.Type = Type.DECIMAL
                temp= tree.addTemporal()
                operation=self.simb(self.Operator.name)
                tree.addExp(temp,izq.value,der.value,operation)
                return Value(temp,Type.DECIMAL,True)



        if self.Operator == ArithmeticOperator.MENOS: #Resta
            # OPERACION SOLO DE ENTEROS
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.ENTERO
                temp= tree.addTemporal()
                operation=self.simb(self.Operator.name)
                tree.addExp(temp,izq.value,der.value,operation)
                return Value(temp,self.getType(),True)

            elif self.OperacionIzq.Type in (Type.ENTERO,Type.DECIMAL) and self.OperacionDer.Type in (Type.ENTERO,Type.DECIMAL):
                self.Type = Type.DECIMAL
                temp= tree.addTemporal()
                operation=self.simb(self.Operator.name)
                tree.addExp(temp,izq.value,der.value,operation)
                return Value(temp,self.getType(),True)

        if self.Operator == ArithmeticOperator.DIV: #DIVISION
            # OPERACION SOLO DE ENTEROS
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.ENTERO
                temp= tree.addTemporal()
                operation=self.simb(self.Operator.name)
                tree.addExp(temp,izq.value,der.value,operation)
                return Value(temp,self.getType(),True)
                    

            elif self.OperacionIzq.Type in (Type.ENTERO,Type.DECIMAL) and self.OperacionDer.Type in (Type.ENTERO,Type.DECIMAL):
                self.Type = Type.DECIMAL
                temp= tree.addTemporal()
                operation=self.simb(self.Operator.name)
                tree.addExp(temp,izq.value,der.value,operation)
                return Value(temp,self.getType(),True)

        if self.Operator == ArithmeticOperator.MOD: #MODULO
            # OPERACION SOLO DE ENTEROS
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.DECIMAL
                temp= tree.addTemporal()
                operation=self.simb(self.Operator.name)
                tree.addExp(temp,izq.value,der.value,operation)
                return Value(temp,self.getType(),True)
                    

        if self.Operator == ArithmeticOperator.POR: #MULTIPLICACION
            # OPERACION SOLO DE ENTEROS
            if self.OperacionIzq.Type == Type.ENTERO and self.OperacionDer.Type == Type.ENTERO:
                self.Type = Type.ENTERO
                temp= tree.addTemporal()
                operation=self.simb(self.Operator.name)
                tree.addExp(temp,izq.value,der.value,operation)
                return Value(temp,Type.ENTERO,True)

            elif self.OperacionIzq.Type in (Type.ENTERO,Type.DECIMAL) and self.OperacionDer.Type in (Type.ENTERO,Type.DECIMAL):
                self.Type = Type.DECIMAL
                temp= tree.addTemporal()
                operation=self.simb(self.Operator.name)
                tree.addExp(temp,izq.value,der.value,operation)
                return Value(temp,Type.DECIMAL,True)
            
            if self.OperacionIzq.Type == Type.CADENA and self.OperacionDer.Type == Type.CADENA:
                self.Type = Type.CADENA
                temp= tree.addTemporal()
                operation=self.simb(self.Operator.name)
                tree.updateConsola(f'\n{temp} = {str(izq.value)} {operation} {str(der.value)} ;')
                return Value(temp,Type.ENTERO,True,(izq.value+der.value))


            elif self.OperacionIzq.Type == Type.CADENA and self.OperacionDer.Type == Type.CADENA:
                pass

        if self.Operator == ArithmeticOperator.POT: # PARA LA POTENCIA
                tree.fPotencia()

                paramTemp = tree.addTemporal()
                tree.addExp(paramTemp,'P',table.size,'+')
                tree.addExp(paramTemp, paramTemp,'1','+')

                tree.setStack(paramTemp,izq.value)
                tree.addExp(paramTemp, paramTemp,'1','+')
                tree.setStack(paramTemp,der.value)

                tree.newEnv(table.size)
                tree.callFun('Potencia')

                tem=tree.addTemporal()
                tree.getStack('P',tem)
                tree.retEnv(table.size)
                return Value(tem,Type.ENTERO,True)

                

                


    #se castea el valor que tiene para que no de error al ejecutarse en el interprete
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
        if Operator=="MAS":
            return "+"
        elif Operator=="MENOS":
            return "-"
        elif Operator=="DIV":
            return "/"
        elif Operator=="POR":
            return "*"
        elif Operator=="POT":
            return "**"
        elif Operator=="MOD":
            return "%"
        elif Operator=="UMENOS":
            return "-"
        elif Operator=="AUMENTO":
            return "++"
        elif Operator=="DECREMENTO":
            return "--"


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
