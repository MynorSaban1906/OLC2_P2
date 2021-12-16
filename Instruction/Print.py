from Expressions.Primitive import Primitive
from Expressions.Id import Id
from typing import ValuesView
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Type import Type
from Abstract.Instruction import Instruction
from SymbolsTable.Table import Table
from SymbolsTable.Exceptions import Exceptions
from Abstract.NodoAST import NodoAST

class Print(Instruction):
    def __init__(self, expression, fila, columna,line=False):
        self.expresion=expression
        self.fila = fila
        self.columna = columna
        self.line=line

    def interpreter(self, tree, table):
        cadena=""
        aux=[]
        if self.expresion==None:
            tree.addPrint("c", 10)

        for x in self.expresion:
            value = x.interpreter(tree, table)  # RETORNA CUALQUIER VALOR para imprimir
            

            if isinstance(value,Primitive):
                value=value.interpreter(tree,table)
                
            # si es un error me generara un error
            if isinstance(value, Exceptions) :
                return value  

            if value.type==Type.ENTERO:
                tree.addPrint("d",value.value)
                break
            elif value.type==Type.DECIMAL:
                tree.addPrintF("f",value.value)
                break

            elif value.type==Type.BOOLEANO :
                tempfinal= tree.addLiteral()
                
                tree.putLabel(value.true_label)
                tree.printTrue()

                tree.addGoto(tempfinal)
                
                tree.putLabel(value.false_label)
                tree.printFalse()

                tree.putLabel(tempfinal)
                

            
            elif value.type==Type.CADENA:
                tree.fPrintString()
                paramTemp = tree.addTemporal()
                tree.addExp(paramTemp,'P',table.size,'+')
                tree.addExp(paramTemp, paramTemp,'1','+')

                tree.setStack(paramTemp,value.value)

                tree.newEnv(table.size)
                tree.callFun('printString')

                tem=tree.addTemporal()
                tree.getStack('P',tem)
                tree.retEnv(table.size)

                



        # actualiza lo que saldra en consola
        if(self.getLine()):# si es println se da un salto de linea 
            
            tree.addPrint("c", 10)

        

    def getNodo(self):
        nodo=NodoAST("RPRINT")
        nodo.Agregar_Primer_Hijo("print")
        nodo.Agregar_Hijo("(")

        for x in self.expresion:
            nodo.Agregar_Hijo_Nodo(x.getNodo())
        
        nodo.Agregar_Hijo(")")
        nodo.Agregar_Hijo(";")
        return nodo
        


    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila= fila 

    def getLine(self):
        return self.line

    def setLine(self, line):
        self.line=line

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna= columna
        

    def getExpresion(self):
        return self.expresion

    def setExpresion(self, expresion):
        self.expresion=expresion 





