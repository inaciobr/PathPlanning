import numpy as np
import matplotlib.pyplot as plt

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
        self.plotMaze()

 
    def loadMaze(self):
        pass


    @classmethod
    def create(cls):
        interface = cls()
        interface.show()

        return interface


    def printMaze(self):
        field = np.where(self.controller.field.mask, ' ', '#')

        # Veículos
        for label, vehicle in self.controller.vehicles.items():
            for step in vehicle.path:
                field[step['position']] = step['action']
                print(step['action'])

            field[vehicle.position] = label

        # Identificação das colunas
        mapa = "     " \
             + ' '.join("{:03}".format(i) for i in range(field.shape[1])) \
             + '\n'

        np.set_printoptions(formatter = {
            'all': lambda x: "| " + x
        })

        # Identificação das linhas e as linhas
        mapa += '\n'.join((
                    "{:03}".format(i) + str(line).replace('[', ' ').replace(']', ' ')
                ) for i, line in enumerate(field))

        print(mapa)


    def plotMaze(self):
        grid = np.full((*self.controller.field.field.shape, 3), 255, dtype = 'i8')
        grid[~self.controller.field.mask] = (0, 0, 0)

        for label, vehicle in self.controller.vehicles.items():
            for step in vehicle.path:
                grid[step['position']] = (0, 255, 0)

            grid[vehicle.position] = (255, 0, 0)
            grid[vehicle.goalPosition] = (0, 0, 255)


        fig, ax = plt.subplots()
        ax.imshow(grid)

        plt.show()