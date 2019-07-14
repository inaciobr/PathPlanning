import numpy as np

"""
Classe utilizada para criar e controlar o campo utilizado para o Path Planning.
Especificações do field:
* '0.0'     => Free space
* 'np.inf'  => Obstacle
"""
class Field:
    def __init__(self, shape):
        self.field = np.zeros(tuple(np.clip(shape, 1, None)))


    def __str__(self):
        return "mapa"

    # Gera um labirinto aleatório.
    @classmethod
    def createMaze(cls, shape, fillPercentage):
        f = cls(shape)
        f.field = np.where(np.random.rand(*f.field.shape) <= min(max(0.0, fillPercentage), 1.0), np.inf, 0.0)
        return f


    # Carrega informações sobre um labirinto. TODO
    @classmethod
    def loadField(cls, file):
        pass

    # Realiza o preprocessamento do mapa.
    def preprocessMaze(self):
        pass


    # Retorna uma tupla com uma posição válida aleatória no mapa.
    def randomPosition(self):
        pass


    # Verifica se é possível traçar um caminho conectando dois pontos.
    def isReachable(self, pos1, pos2):
        pass
