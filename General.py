
class General:

    tempo = None

    def __init__(self):
        self.contadorTemp=0
        self.c3d=""
        self.temporary=[]
    
    def textHeader(self):
        self.c3d= """
                    // ------------- HEADER ----------------- 
                    package main
                    import (
                        "fmt"
                    )
                    """

    def textVars(self):
        self.c3d+="var "
        for x in self.temporary:
            self.c3d+='f {x}'
            if x.index(x)==self.contadorTemp:
                self.c3d+=" , "
        self.c3d+=" float64;\n"

    def gettextC3D(self):
        return self.c3d

    def main(self):
        self.c3d+=""" // ------------- MAIN -----------------
            func main() {
        """
    def addTemporal(self):
        tem=f't{self.contadorTemp}'
        self.contadorTemp+=1
        self.temporary.append(tem)
        return tem
    
    def get_instance(self):
        if General.tempo==None:
            re= General.tempo= General()
            return re
        else:
            return General.tempo

    def addExpression(self,temp,operator,left,right):
        string=f'{temp} = {left} {operator} {right} ; '



        