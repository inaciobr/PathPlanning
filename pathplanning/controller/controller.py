from ..field import Field, Drone
from .. import AI

import numpy as np

import cProfile
import time


class Controller:  
    def __init__(self):
        self.field = None
        self.vehicles = { }

    
    def createMaze(self, shape, fillPercentage):
        #print(Search.straightLine(self.vehicles['A'].position, self.vehicles['A'].goalPosition, self.actions, self.field))
        #self.field = Field.load('tAcess.npy')
        #test = np.array([[0, 0, 0, 0, 0], [0, 0, np.inf, np.inf, np.inf], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
        #self.field = Field(test)
        self.field = Field.createMaze((1000, 1000), 0.1)
        self.addDrone('A', (0, 0)).setGoal((999, 999))
        t = time.time()
        #AI.AStar(self.vehicles['A'].position, self.vehicles['A'].goalPosition, self.field, self.actions)
        for _ in range(1):
            #self.vehicles['A'].path = AI.AStar((0, 0), (999, 999), self.field, AI.getFourMoves())
            self.vehicles['A'].path = AI.iterativeGeneticSearch((0, 0), (999, 999), self.field, AI.getFourMoves())
            #AI.depthFirst((0, 0), (199, 199), self.field.mask, AI.getFourMoves())

            #AI.straightLinePositions((0, 0), (999, 999), self.field.mask)
            #AI.connectedComponentLabeling(self.field.mask)
            #self.field = Field.createMaze((200, 200), 0.2)
            #if np.any(AI.connectedComponentLabeling(self.field.mask) != ndimage.measurements.label(self.field.mask)[0]):
            #    print("AAAAAAAAAAAAAAAAAAAAA")

        print(time.time() - t)

        #self.field = Field.createMaze((1000, 1000), 0.2)
        #self.field = Field.load('tAcess.npy')
        #self.addDrone('A', (0, 0)).setGoal((999, 999))
        #print(Search.AStar(self.vehicles['A'].position, self.vehicles['A'].goalPosition, self.actions, self.field))
        #print(self.field.field[:10, :10])
        #print(self.field.region[:10, :10])
        #print(self.field.isReachable((0, 0), (999, 999)))"""
        
        """cProfile.runctx("AStar(start, goal, field, actions)", {
            'AStar': AI.AStar
        }, {
            'start': (0, 0),
            'goal': (999, 999),
            'field': self.field,
            'actions': AI.getFourMoves()
        }, sort='cumtime')

        
        #print((self.vehicles['A']))
        #self.field.save('test')"""

    
    def addDrone(self, label, position):
        d = Drone(label, position)
        self.vehicles[label] = d
        return d
