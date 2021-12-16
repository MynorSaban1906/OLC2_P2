from Abstract.Instruction import Instruction
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Type import Type
from SymbolsTable.Symbols import Symbols
from Instruction.Continue import Continue
from Instruction.Break import Break
from Instruction.Return import Return
from SymbolsTable.Table import Table
from Abstract.NodoAST import NodoAST

class While(Instruction):
    def __init__(self, Conditional, Instr, Row, Column):
        self.Conditional = Conditional
        self.Instr = Instr
        self.Row = Row
        self.Column = Column

    def interpreter(self, tree, table):
        
        continueLb= tree.addLiteral()
        tree.putLabel(continueLb)

        Conditional = self.getConditional().interpreter(tree, table)
        if isinstance(Conditional, Exceptions): return Conditional

        if self.getConditional().Type == Type.BOOLEANO:
            nuevaTabla = Table(table,entorno="WHILE",declaracionTipo="variable",Row=self.Row,Column=self.Column)      #NUEVO ENTORNO
            nuevaTabla.breaklb=Conditional.false_label
            
            nuevaTabla.continuelb= continueLb

            tree.putLabel(Conditional.true_label)


            for instruccion in self.Instr:
                result = instruccion.interpreter(tree,nuevaTabla)
                if isinstance(result,Exceptions):
                    tree.getExcepciones().append(result)
                if isinstance(result,Break): return None
                if isinstance(result,Return): return None
                if isinstance(result,Continue): break

            tree.addGoto(continueLb)
            tree.putLabel(Conditional.false_label)
        else:
            return Exceptions("Semantico", "Type de dato no booleano en while.", self.Row, self.Column)


    def getNodo(self):
        nodo=NodoAST("WHILE")

        instrucciones=NodoAST("INSTRUCCIONES")
        for instr in self.Instr:
            instrucciones.Agregar_Hijo_Nodo(instr.getNodo())

        nodo.Agregar_Hijo_Nodo(instrucciones)
        
        return nodo


    def getRow(self):
        return self.Row

    def setRow(self, Row):
        self.Row= Row 

    def getColumn(self):
        return self.Column

    def setColumn(self, Column):
        self.Column= Column

    def getConditional(self):
        return self.Conditional

    def setConditional(self, COnditional):
        self.Conditional=COnditional

    def getInstr(self):
        return self.Instr

    def setInstr(self, Instr):
        self.Instr =Instr