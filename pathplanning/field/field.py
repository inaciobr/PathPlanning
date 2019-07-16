from .preprocess import Preprocess

import numpy as np
import random


__all__ = ['Field']

"""
Classe utilizada para criar e controlar o campo utilizado para o Path Planning.
Especificações do field:
* '0.0'     => Free space
* 'np.inf'  => Obstacle
"""
class Field:
    """
    Inicialização do campo
    """
    def __init__(self, field):
        self.field = field


    # Gera um labirinto aleatório
    @classmethod
    def createMaze(cls, shape, fillPercentage):
        mask = np.random.rand(*np.clip(shape, 1, None)) <= fillPercentage
        return cls(np.where(mask, np.inf, 0.0))


    """
    Salvar e carregar campo
    """
    # Carrega informações sobre um campo
    @classmethod
    def load(cls, file):
        return cls(np.load(file))


    # Salva informações sobre um campo
    def save(self, file):
        np.save(file, self.field)


    """
    Métodos relevantes para o campo
    """
    # Retorna uma tupla com uma posição válida aleatória no mapa
    def randomPosition(self):
        pos = random.randrange(0, self.validPositionsAmount)
        return (self.validPositions[0][pos], self.validPositions[1][pos])


    # Verifica se é possível traçar um caminho conectando dois pontos
    def isReachable(self, pos1, pos2):
        return self.region[pos1] == self.region[pos2] and self._field[pos1] != np.inf


    # Retorna as posições vizinhas de um nó
    def getNeighbors(self, position, actions, pathCost = 0):
        for action in actions:
            edgePos = (position[0] + action['direction'][0], position[1] + action['direction'][1])

            if 0 <= edgePos[0] < self._field.shape[0] and 0 <= edgePos[1] < self._field.shape[1] and self.mask[edgePos]:
                yield {'position': edgePos,
                       'pathCost': action['cost'] + pathCost,
                       'action': action['action']}


    """ 
    Atributos
    """
    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, value):
        self._field = value
        self.shape = value.shape

        # Preprocess
        self.mask = self._field != np.inf
        self.validPositions = Preprocess.validPositions(self.mask)
        self.validPositionsAmount = self.validPositions[0].size
        self.region = Preprocess.connectedComponent(self.mask)


    # Exibe o campo
    def __str__(self):
        np.set_printoptions(formatter = { 'float': lambda x: '| ' + str('#' if x == np.inf else ' ') })

        # Identificação das colunas
        mapa = '     ' + ' '.join("{:03}".format(i) for i in range(self.shape[1])) + '\n'

        # Identificação das linhas e as linhas
        mapa += '\n'.join(("{:03}".format(i) + str(line).replace('[', ' ').replace(']', ' ')) for i, line in enumerate(self.field))

        return mapa
