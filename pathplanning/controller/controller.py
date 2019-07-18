from ..field import Field, Drone
from ..AI import Search

import cProfile
import time


class Controller:
    def __init__(self):
        self.field = None
        self.vehicles = { }

    
    def createMaze(self, shape, fillPercentage):
        """self.field = Field.createMaze((1000, 1000), 0.0)
        self.addDrone('A', (0, 0)).setGoalPosition((500, 500))
        #print(Search.straightLine(self.vehicles['A'].position, self.vehicles['A'].goalPosition, self.vehicles['A'].actions, self.field))
        #self.field = Field.load('tAcess.npy')
        t = time.time()
        for _ in range(1000):
            Search.checkStraightLine(self.vehicles['A'].position, self.vehicles['A'].goalPosition, self.field)
        print(time.time() - t)"""

        #self.field = Field.createMaze((1000, 1000), 0.2)
        self.field = Field.load('tAcess.npy')
        self.addDrone('A', (0, 0)).setGoalPosition((999, 999))
        #print(self.field.field[:10, :10])
        #print(self.field.region[:10, :10])
        #print(self.field.isReachable((0, 0), (999, 999)))
        
        cProfile.runctx("AStar(start, goal, actions, field)", {
            'AStar': Search.AStar
        }, {
            'start': self.vehicles['A'].position,
            'goal': self.vehicles['A'].goalPosition,
            'actions': self.vehicles['A'].actions,
            'field': self.field
        })

        
        #print((self.vehicles['A']))
        #self.field.save('test')"""

    
    def addDrone(self, label, position):
        d = Drone(label, position)
        self.vehicles[label] = d
        return d
