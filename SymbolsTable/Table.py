from SymbolsTable.Type import Type
from SymbolsTable.Exceptions import Exceptions
from SymbolsTable.Symbols import Symbols

tablaS=[]
class Table:
    

    def __init__(self, anterior = None,entorno=None,declaracionTipo=None,Row=None,Column=None):
        self.tabla = {} # Diccionario Vacio
        self.anterior = anterior
        self.entorno=entorno
        self.descripcion=declaracionTipo
        self.Row=Row
        self.Column=Column
        self.breaklb=''
        self.continuelb=''
        self.size=0
        if self.anterior!=None:
            self.breaklb=self.anterior.breaklb
            self.continuelb=self.anterior.continuelb
            self.size=self.anterior.size



    def setTabla(self, id, type, row, column, value,inHeap ,value2,ntabla):      # Agregar una variable
        tablaActual = self
        if id in self.tabla :
            return Exceptions("Semantico", "Variable " + id + " ya existe",row, column,)
        else:
            self.tabla[id] = Symbols(id,type,row,column,value,self.size,tablaActual==None,inHeap,value2)
            t=repo(id,ntabla.descripcion,ntabla.entorno,row,column)
            self.size+=1
            for x in tablaS:
                
                if x.id== t.id and x.entorno==t.entorno:
                    return None
            else:
                tablaS.append(t)
                return None
    
    def SearchAux(self,id):
        tablaActual = self
        while tablaActual != None: 
            if id in tablaActual.tabla :
                return True
            else:
                tablaActual = tablaActual.anterior
        return False

    def getTabla(self, id):            # obtener una variable
        tablaActual = self
        while tablaActual != None:
            if id in tablaActual.tabla :
                return tablaActual.tabla[id]           # RETORNA SIMBOLO
            else:
                tablaActual = tablaActual.anterior
        return None

    def getTablaLocal(self, id):            # obtener una variable
        tablaActual = self
        if id in tablaActual.tabla :
            return tablaActual.tabla[id]           # RETORNA SIMBOLO
        else:

            return None


    def updateTable(self, simbolo):
        tablaActual = self
        while tablaActual != None: 
            if simbolo.id in tablaActual.tabla :
                tablaActual.tabla[simbolo.id].setValue(simbolo.getValue())
                tablaActual.tabla[simbolo.id].setType(simbolo.getType())
                    
                return None
            else:
                tablaActual = tablaActual.anterior
        return Exceptions("Semantico", "Variable No encontrada en Asignacion", simbolo.getgetRow()(), simbolo.getgetColumn()())


    def reporteSimbolos(self,value):
        
        if value not in tablaS:
            tablaS.append(value)

    def generareporte(self):
        return tablaS

class repo():
    def __init__(self, id,descripcion,entorno,row,column):
        self.id= id
        self.entorno=entorno
        self.descripcion=descripcion
        self.Row=row
        self.Column=column

    def toString(self):
        return " > " +self.id + "  - Description " + self.descripcion +" entorno "+self.entorno+ "  in [" + str(self.Row) + "," + str(self.Column) + "]" 

