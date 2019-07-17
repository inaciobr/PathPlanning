from ..controller import Controller

class Interface:
    def __init__(self):
        self.controller = Controller()


    def show(self):
        print("===== Path Planning =====")
        self.createMaze()
        
        #self.printMaze()


    def createMaze(self):
        shape = (10, 10)
        fillPercentage = 0.0
        self.controller.createMaze(shape, fillPercentage)

 
    def loadMaze(self):
        pass


    def printMaze(self):
        print(self.controller.field)

 
    @classmethod
    def create(cls):
        interface = cls()
        interface.show()
        return interface
