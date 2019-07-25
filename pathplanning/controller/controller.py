from ..field import Field, Drone
from .. import AI

import cProfile
import time


class Controller:
    actions = [
        { 'action': '^', 'cost': 1, 'direction': (-1,  0), 'hash': 0x01 },
        { 'action': 'v', 'cost': 1, 'direction': (+1,  0), 'hash': 0x02 },
        { 'action': '<', 'cost': 1, 'direction': ( 0, -1), 'hash': 0x04 },
        { 'action': '>', 'cost': 1, 'direction': ( 0, +1), 'hash': 0x08 },
        #{ 'action': 'o', 'cost': 1, 'direction': ( 0,  0), 'hash': 0x10 },
    ]
    
    def __init__(self):
        self.field = None
        self.vehicles = { }

    
    def createMaze(self, shape, fillPercentage):
        #print(Search.straightLine(self.vehicles['A'].position, self.vehicles['A'].goalPosition, self.actions, self.field))
        #self.field = Field.load('tAcess.npy')
        self.field = Field.createMaze((200, 200), 0.0)
        self.addDrone('A', (0, 0)).setGoal((999, 999))
        t = time.time()
        #AI.AStar(self.vehicles['A'].position, self.vehicles['A'].goalPosition, self.field, self.actions)
        for _ in range(100):
            AI.straightLine((0, 0), (199, 199), self.field, self.actions)
            #AI.breadthFirst((0, 0), (199, 199), self.field.mask)
        print(time.time() - t)

        #self.field = Field.createMaze((1000, 1000), 0.2)
        #self.field = Field.load('tAcess.npy')
        #self.addDrone('A', (0, 0)).setGoal((999, 999))
        #print(Search.AStar(self.vehicles['A'].position, self.vehicles['A'].goalPosition, self.actions, self.field))
        #print(self.field.field[:10, :10])
        #print(self.field.region[:10, :10])
        #print(self.field.isReachable((0, 0), (999, 999)))
        
        """cProfile.runctx("AStar(start, goal, field, actions)", {
            'AStar': Search.AStar
        }, {
            'start': self.vehicles['A'].position,
            'goal': self.vehicles['A'].goalPosition,
            'field': self.field,
            'actions': self.actions
        })

        
        #print((self.vehicles['A']))
        #self.field.save('test')"""

    
    def addDrone(self, label, position):
        d = Drone(label, position)
        self.vehicles[label] = d
        return d
