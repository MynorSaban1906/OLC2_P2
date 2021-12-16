import re
from SymbolsTable.Table import repo
from General import General
class Tree:
    def __init__(self, instrucciones ):
        self.instrucciones = instrucciones # son de tipo instrucciones
        self.excepciones = [] #para las excepciones, estas se guardan en objetos en esta tabla
        self.funciones=[] # lista para las funciones guardadas
        # consola = codigo de 3 direcciones
        self.consola = ""  #aqui se encuentra el consola
        self.codeFun=""
        self.natives= ''
        self.inFun=False
        self.inNatives=False
        self.temporary=[]  # aqui se encuentran las t0, t1 ,/................
        self.contadorTemp=0 # contador de los temporales
        self.contadorLite= 0# contador de literal
        self.TablaSimboloGlobal = None # al inicial inicia en NOne
        self.printString=False
        self.punteroStack=0
        self.potencia=False
        self.lowercase=False
        self.uppercase=False
        self.size=0  # PARA EL CAMBIO DE ENTORNO 



  
    def getInstrucciones(self):
        return self.instrucciones

    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones

    def getExcepciones(self):
        return self.excepciones

    def setExcepciones(self, excepciones):
        self.excepciones = excepciones

    def getConsola(self):
        return self.consola
    
    def setConsola(self, consola):
        self.consola = consola

    def updateConsola(self,cadena):
        self.consola += str(cadena)

    def getTablaSimboloGlobal(self):
        return self.TablaSimboloGlobal
    
    def setTablaSimboloGlobal(self, TablaSimboloGlobal):
        self.TablaSimboloGlobal = TablaSimboloGlobal


    def getFunciones(self):
        return self.funciones

    def getFuncion(self, identificador):
        for funcion in self.funciones:
            if funcion.getId() == identificador:
                return funcion
        return None
    
    def addFuncion(self, funcion):
        self.funciones.append(funcion)



# implementacion de codigo 3 direcciones 
    def getHeader(self):
        ret = '/*----HEADER----*/\npackage main;\n\nimport (\n\t"fmt"\n)\n\n'
        if len(self.temporary) > 0:
            ret += 'var '
            for temp in range(len(self.temporary)):
                ret += self.temporary[temp]
                if temp != (len(self.temporary) - 1):
                    ret += ", "
            ret += " float64 ; \n"
        ret += "var P, H float64;\nvar stack [30101999]float64;\nvar heap [30101999]float64;\n\n"
        return ret

    def codeIn(self, code, tab="\t"):
        if(self.inNatives):
            if(self.natives == ''):
                self.natives = self.natives + '/*-----NATIVES-----*/\n'
            self.natives = self.natives + tab + code
        elif(self.inFun):
            if(self.codeFun == ''):
                self.codeFun = self.codeFun + '/*-----codeFun-----*/\n'
            self.codeFun = self.codeFun + tab +  code
        else:
            self.consola = self.consola + '\t' +  code

    def getCode(self):
        return f'{self.getHeader()}{self.natives}\n{self.codeFun}\nfunc main(){{\n{self.consola}\n}}'


    def addTemporal(self):
        tem=f't{self.contadorTemp}'
        self.contadorTemp+=1
        self.temporary.append(tem)
        return tem

    def addLiteral(self):
        tem=f'L{self.contadorLite}'
        self.contadorLite+=1
        return tem

   
    def addPrint(self, type, value):
        self.codeIn(f'fmt.Printf("%{type}",int({value}));\n')
        
    def addPrintF(self, type, value):
        self.codeIn(f'fmt.Printf("%{type}",float64({value}));\n')

    def printTrue(self):
        self.addPrint("c",116)
        self.addPrint("c",114)
        self.addPrint("c",117)
        self.addPrint("c",101)

    def printFalse(self):
        self.addPrint("c",102)
        self.addPrint("c",97)
        self.addPrint("c",108)
        self.addPrint("c",115)
        self.addPrint("c",101)

    # sentencia IF
    def addIf(self, left, rigth, op, label):
        self.codeIn(f'if {left} {op} {rigth} {{goto {label};}}\n')

    # goto
    def addGoto(self,label):
        self.codeIn(f'goto {label};\n')

    def putLabel(self,label):
        self.codeIn(f'{label}:\n')

    def addExp(self,tem, left, right,op):
        self.codeIn(f'{tem}= {left} {op} {right};\n')

    def setStack(self,puntero, valor):
        self.codeIn(f'stack [int({puntero})]= {valor};\n')
    
    def getStack(self,puntero,tem):
        self.codeIn(f'{tem} =stack [int({puntero})];\n')
        
    def addH(self):
        self.codeIn('H= H+1;\n')
        
    def addComment(self, comment):
        self.codeIn(f'/* {comment} */\n')

    def addP(self):
        tem=self.size
        self.size+=1
        return tem
    
    def quitP(self):
        self.punteroStack-=1
        
    def addBeginFunc(self,date):
        if not self.inNatives:
            self.inFun= True
        self.codeIn(f'func {date}()' + "{\n")

    def addEndFunc(self):
        self.codeIn('return;\n}\n')
        if not self.inNatives:
            self.inFun=False 

    def getHeap(self,tem,puntero):
        self.codeIn(f'{tem} =heap [int({puntero})];\n')
      
    def setHeap(self,tem,puntero):
        self.codeIn(f'heap [int({puntero})]={tem};\n')

    def fPrintString(self):
        if self.printString:
            return 
        self.printString=True
        self.inNatives=True

        self.addBeginFunc('printString')

        #para poder salid de la funcion
        returnLbL = self.addLiteral()
        #para la comparacion para buscar fin de cadena
        compareLbl = self.addLiteral()

        #temporal de puntero a stack
        tempP=self.addTemporal()
        #temporal para el puntero a Heap
        tempH=self.addTemporal()

        self.addExp(tempP,'P','1','+')

        self.getStack(tempP,tempH)

        #temporal para comparar
        tempC= self.addTemporal()
        self.putLabel(compareLbl)
        self.getHeap(tempC,tempH)
        self.addIf(tempC,'-1','==',returnLbL)

        self.addPrint('c',tempC)

        self.addExp(tempH,tempH,'1','+')

        self.addGoto(compareLbl)

        self.putLabel(returnLbL)
        self.addEndFunc()
        self.inNatives=False

    def newEnv(self,size_):
        self.codeIn(f'P=P+{size_};\n')

    def retEnv(self,size_):
        self.codeIn(f'P=P-{size_};\n')

    def callFun(self,value):
        self.codeIn(f'{value}();\n')

    def flowercase(self):
        if self.lowercase:
            return 
        self.lowercase= True
        self.inNatives=True
        self.addBeginFunc('lowercase')
        t1= self.addTemporal()
        self.addExp(t1,'H','','')
        t2=self.addTemporal()
        self.addExp(t2,'P','1','+')
        self.getStack(t2,t2)

        L0=self.addLiteral()
        self.putLabel(L0)

        L2=self.addLiteral()
        L1=self.addLiteral()


        t3=self.addTemporal()
        self.getHeap(t3,t2)

        self.addIf(t3,'-1','==',L2)
        self.addIf(t3,'65','<',L1)
        self.addIf(t3,'90','>',L1)


        self.addExp(t3,t3,'32','+')

        self.putLabel(L1)

        self.setHeap(t3,'H')
        self.addH()

        self.addExp(t2,t2,'1','+')
        self.addGoto(L0)

        self.putLabel(L2)
        self.setHeap('-1','H')
        self.addH()
        self.setStack('P',t1)
        self.addEndFunc()
        self.inNatives=False

    def fuppercase(self):
        if self.uppercase:
            return 
        self.uppercase= True
        self.inNatives=True
        self.addBeginFunc('uppercase')
        t1= self.addTemporal()
        self.addExp(t1,'H','','')
        t2=self.addTemporal()
        self.addExp(t2,'P','1','+')
        self.getStack(t2,t2)

        L0=self.addLiteral()
        self.putLabel(L0)

        L2=self.addLiteral()
        L1=self.addLiteral()


        t3=self.addTemporal()
        self.getHeap(t3,t2)

        self.addIf(t3,'-1','==',L2)
        self.addIf(t3,'97','<',L1)
        self.addIf(t3,'122','>',L1)


        self.addExp(t3,t3,'32','-')

        self.putLabel(L1)

        self.setHeap(t3,'H')
        self.addH()

        self.addExp(t2,t2,'1','+')
        self.addGoto(L0)

        self.putLabel(L2)
        self.setHeap('-1','H')
        self.addH()
        self.setStack('P',t1)
        self.addEndFunc()
        self.inNatives=False


    def fPotencia(self):
        if self.potencia:
            return 
        
        self.potencia==True
        self.inNatives=True

        self.addBeginFunc('Potencia')

        t0=self.addTemporal()

        self.addExp(t0,'P',1,'+')

        t1= self.addTemporal()

        self.getStack(t0,t1)

        self.addExp(t0,t0,'1','+')

        t2= self.addTemporal()
        self.getStack(t0,t2)

        self.addExp(t0,t1,'','')

        t3= self.addTemporal()
        self.addExp(t3,'P',2,'+')
        self.getStack(t3,t2)
        
        L0=self.addLiteral()
        L1=self.addLiteral()
        L2=self.addLiteral()
        L3=self.addLiteral()


        self.addIf(t2, '0', '==', L0)
        self.putLabel(L1)
        self.addIf(t2, '1', '<=', L2)
        self.addExp(t1, t1, t0, '*')
        self.addExp(t2, t2, '1', '-')
        self.addGoto(L1)

        self.putLabel(L2)
        self.setStack('P', t1)
        self.addGoto(L3)
        self.putLabel(L0)
        self.setStack('P',1)
        self.putLabel(L3)
        self.addEndFunc()
        self.inNatives=False