from Abstract.Instruction import Instruction
from SymbolsTable.Type import Type
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Table import Table
from Instruction.Break import Break
from Instruction.Continue import Continue
from Instruction.Return import Return
from Abstract.NodoAST import NodoAST





class If(Instruction):
    def __init__(self, condicion, instruccionesIf, Row, Column,instruccionesElse=None):
        self.condicion = condicion
        self.instruccionesIf = instruccionesIf
        self.instruccionesElse = instruccionesElse
        self.Row = Row
        self.Column = Column

    def interpreter(self, tree, table):
        tree.addComment("se empieza el if ")
        condicion = self.condicion.interpreter(tree, table)
        if isinstance(condicion, Exceptions): return condicion

        if self.condicion.Type == Type.BOOLEANO:
            nuevaTabla = Table(table,entorno="IF",declaracionTipo="variable",Row=self.Row,Column=self.Column)       #NUEVO ENTORNO
            
            tree.putLabel(condicion.true_label)
            
            self.instruccionesIf.interpreter(tree,table)

            if self.instruccionesElse!=None:
                exitIf=tree.addLiteral()
                tree.addGoto(exitIf)

            tree.putLabel(condicion.false_label)
                
            if self.instruccionesElse!=None:
                self.instruccionesElse.interpreter(tree,table)
                tree.putLabel(exitIf)
                

        else:
            return Exceptions("Semantico", "Type de dato no booleano en IF.", self.Row, self.Column)




    def getNodo(self):
        nodo=NodoAST("IF")

        instruccionesIf=NodoAST("INSTRUCCIONES IF")
        for instr in self.instruccionesIf:
            instruccionesIf.Agregar_Hijo_Nodo(instr.getNodo())
        nodo.Agregar_Hijo_Nodo(instruccionesIf)

        if self.instruccionesElse != None:
            instruccionesElse=NodoAST("INSTRUCCIONES ELSE")
            for instr in self.instruccionesElse:
                instruccionesElse.Agregar_Hijo_Nodo(instr.getNodo())
            nodo.Agregar_Hijo_Nodo(instruccionesElse)

        elif self.elseIf != None:
            nodo.Agregar_Hijo_Nodo(self.elseIf.getNodo())
        
        return nodo