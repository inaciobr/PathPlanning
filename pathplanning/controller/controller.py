from ..field import Field, Drone


class Controller:
    def __init__(self):
        self.field = None
        self.vehicles = { }

    
    def createMaze(self, shape, fillPercentage):
        self.field = Field.createMaze(shape, fillPercentage)

    
    def addDrone(self, label, position):
        self.vehicles[label] = Drone(label, position)
