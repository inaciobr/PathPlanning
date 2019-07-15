from .preprocess import Preprocess

import numpy as np
import random

"""
Classe utilizada para criar e controlar o campo utilizado para o Path Planning.
Especificações do field:
* '0.0'     => Free space
* 'np.inf'  => Obstacle
"""
class Field:
    def __init__(self, field):
        self.field = field
        self.vehicles = [ ]


    # Gera um labirinto aleatório.
    @classmethod
    def createMaze(cls, shape, fillPercentage):
        mask = np.random.rand(*np.clip(shape, 1, None)) <= min(max(0.0, fillPercentage), 1.0)
        return cls(np.where(mask, np.inf, 0.0))


    # Carrega informações sobre um campo. TODO
    @classmethod
    def loadField(cls, file):
        pass


    # Salva informações sobre um campo. TODO
    def saveField(self, file):
        pass


    # Retorna uma tupla com uma posição válida aleatória no mapa.
    def randomPosition(self):
        pos = random.randrange(0, self.validPositionsAmount)
        return (self._validPositions[0][pos], self._validPositions[1][pos])


    # Verifica se é possível traçar um caminho conectando dois pontos.
    def isReachable(self, pos1, pos2):
        return self.region[pos1] == self.region[pos2] != np.inf



    """
    Atributos
    """
    @property
    def field(self):
        return self._field


    @property
    def shape(self):
        return self.field.shape


    @property
    def mask(self):
        return self._mask


    @property
    def validPositionsAmount(self):
        return self._validPositions[0].size


    @property
    def validPositions(self):
        return self._validPositions


    @property
    def region(self):
        return self._region


    @field.setter
    def field(self, value):
        self._field = value

        # Preprocess
        self._mask = self.field != np.inf
        self._validPositions = Preprocess.validPositions(self.mask)
        self._region = Preprocess.connectedComponent(self.field)


    # Exibe o campo no terminal.
    def __str__(self):
        np.set_printoptions(formatter = { 'float': lambda x: '| ' + str('#' if x == np.inf else ' ') })

        # Identificação das colunas
        mapa = '     ' + ' '.join("{:03}".format(i) for i in range(self.shape[1])) + '\n'

        # Identificação das linhas e as linhas
        mapa += '\n'.join(("{:03}".format(i) + str(line).replace('[', ' ').replace(']', ' ')) for i, line in enumerate(self.field))
        
        print(self.randomPosition())
        return mapa
