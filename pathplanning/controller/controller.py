from ..field import Field, Drone
from ..AI import *

import cProfile


class Controller:
    def __init__(self):
        self.field = None
        self.vehicles = { }

    
    def createMaze(self, shape, fillPercentage):
        self.field = Field.createMaze((5, 5), 0.0)
        self.addDrone('A', (0, 0)).setGoalPosition((4, 4))
        print(AStar(self.vehicles['A'].position, self.vehicles['A'].goalPosition, self.vehicles['A'], self.field))

        """#self.field = Field.createMaze((1000, 1000), 0.2)
        self.field = Field.load('tAcess.npy')
        self.addDrone('A', (0, 0)).setGoalPosition((999, 999))
        #print(self.field.field[:10, :10])
        #print(self.field.region[:10, :10])
        #print(self.field.isReachable((0, 0), (999, 999)))
        
        cProfile.runctx("AStar(start, goal, obj, maze)", {
            'AStar': AStar
        }, {
            'start': self.vehicles['A'].position,
            'goal': self.vehicles['A'].goalPosition,
            'obj': self.vehicles['A'],
            'maze': self.field
        })

        
        #print((self.vehicles['A']))
        #self.field.save('test')"""

    
    def addDrone(self, label, position):
        d = Drone(label, position)
        self.vehicles[label] = d
        return d
