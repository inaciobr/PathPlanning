from ..field import Field

class Interface():
    def __init__(self):
        self.field = None


    def show(self):
        print("===== Path Planning =====")
        self.createMaze()
        self.printMaze()


    def createMaze(self):
        shape = (5, 5)
        fillPercentage = 0.2
        self.field = Field.createMaze(shape, fillPercentage)


    def loadMaze(self):
        file = 'file'
        self.field = Field.loadField(file)


    def printMaze(self):
        print(self.field)


    @classmethod
    def create(cls):
        interface = cls()
        interface.show()
        return interface
