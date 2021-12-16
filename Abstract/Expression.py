from abc import ABC, abstractmethod

class Expression(ABC):
    
    def __init__(self, line, column):
        self.Row = line
        self.Column = column
        self.trueLb = ''
        self.falseLb = ''
        self.structType = ''
    
    @abstractmethod
    def interpreter(self, tree, table):
        pass
