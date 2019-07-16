from ..field import Field, Drone


class Controller:
    def __init__(self):
        self.field = None
        self.vehicles = { }

    
    def createMaze(self, shape, fillPercentage):
        self.field = Field.createMaze(shape, fillPercentage)
        self.addDrone('A', (2, 2))
        print((self.vehicles['A']))

    
    def addDrone(self, label, position):
        self.vehicles[label] = Drone(label, position)
