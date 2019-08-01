from .include import geneticAlgorithm
from . import preprocess
from . import straight
from . import cost
from . import path

import numpy as np
import numba as nb

__all__ = ['geneticSearch']


@nb.njit(nb.int64[:](nb.int32[:, :], nb.types.UniTuple(nb.int64[:], 2))) # Parallel?
def fit(idx, positions):
    fitness = np.zeros(idx.shape[1], dtype=nb.int64)
    x, y = positions

    for i in range(fitness.size):
        fitness[i] += cost.manhattanDistance((x[0], y[0]), (x[idx[0, i]], y[idx[0, i]])) \
                    + cost.manhattanDistance((x[idx[-1, i]], y[idx[-1, i]]), (x[-1], y[-1]))

    #for i, j in np.ndindex(idx.shape):
    #    fitness[i] = cost.manhattanDistance((x[0], y[0]), (x[-1], y[-1]))

    return fitness


def geneticSearch(start, goal, field, actions):
    populationSize = 30

    # Tentativa 0 (Linha reta)
    if straight.checkStraightLine(start, goal, field.mask):
        return straight.straightLine(start, goal, field, actions)

    # Obtém regiões do mapa
    regions = preprocess.connectedComponentLabeling(field.mask)

    # Verifica se os pontos são acessíveis
    if regions[start] != regions[goal] or regions[start] == 0:
        return path.makePath(None)

    mask = regions == regions[start]
    mask[start] = False
    mask[goal] = False

    # Obtém lista de posições válidas
    # Posição inicial estará sempre no índice 0
    # Posição final estará sempre no índice -1
    validPositions = mask.nonzero()
    numPositions = validPositions[0].size

    validPositions = list(zip(*validPositions))
    validPositions.append(goal)
    validPositions.insert(0, start)

    # Tentativa 1 (1 ponto intermediário)
    population = np.random.randint(1, numPositions, (populationSize, 1))
    fitness = fit(population.T, tuple(np.array(validPositions).T))
    #print(fitness)

    return path.makePath(None)
