from abc import ABC, abstractmethod



class Instruction(ABC):
    def __init__(self, Row, Column):
        self.Row = Row
        self.Column = Column
        self.arreglo=False
        self.true_label=''
        self.false_label=''
        super().__init__()

    @abstractmethod
    def interpreter(self, tree, table):
        pass

    @abstractmethod
    def getNodo(self):
        pass