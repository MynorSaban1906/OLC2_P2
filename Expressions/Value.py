
class Value:

    def __init__(self,value,type,is_temp,result="",aux_type=""):
        self.value=value
        self.type=type
        self.is_temp=is_temp
        self.aux_type=aux_type
        self.true_label=''
        self.false_label=''
        self.puntero=0
        self.result=result
        