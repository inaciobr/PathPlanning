from .include import GeneticAlgorithm
from . import preprocess
from . import straight
from . import cost
from . import path

import numpy as np
import numba as nb


__all__ = ['iterativeGeneticSearch']


@nb.njit(nb.int64[:](nb.int32[:, :], nb.types.UniTuple(nb.int64[:], 2)), parallel = True) # Parallel?
def fit(idx, positions):
    fitness = np.zeros(idx.shape[1], dtype=nb.int64)
    x, y = positions # Posições válidas

    for j in nb.prange(fitness.size):
        fitness[j] += cost.manhattanDistance((x[0], y[0]), (x[idx[0, j]], y[idx[0, j]])) \
                    + cost.manhattanDistance((x[idx[-1, j]], y[idx[-1, j]]), (x[-1], y[-1]))

    for i in nb.prange(idx.shape[0] - 1):
        for j in nb.prange(idx.shape[1]):
            fitness[j] += cost.manhattanDistance((x[idx[i, j]], y[idx[i, j]]),
                                                (x[idx[i + 1, j]], y[idx[i + 1, j]]))

    return fitness


def iterativeGeneticSearch(start, goal, field, actions):
    # Tentativa 0 (Linha reta)
    if straight.checkStraightLine(start, goal, field.mask):
        return straight.straightLine(start, goal, field, actions)

    # Obtém regiões do mapa
    regions = preprocess.connectedComponentLabeling(field.mask)
    
    # Verifica se os pontos são acessíveis
    if regions[start] != regions[goal] or regions[start] == 0:
        return path.makePath(None)

    # Obtém posições válidas
    validPositions = listValidPositions(regions, start, goal)

    # Configuração do algoritmo genético
    geneSize = 10           # Pontos intermediáros
    populationSize = 100    # Número de indivíduos
    maxIteractions = 500    # Número de interações
    threshold = 0.0         # Valor para encerrar algoritmo

    # Algoritmo Genético
    GA = GeneticAlgorithm(
        # Função a ser minimizada
        fitnessFunction = fit,
        arg = validPositions,
        lowerBound = 1,
        upperBound = validPositions[0].size - 1,

        # Parâmetros de ajuste do GA
        geneSize = geneSize,
        maxIteractions = maxIteractions,
        populationSize = populationSize,
        eliteSize = populationSize // 20,
        threshold = threshold,

        # Parâmetros de ajustes dos métodos
        selectionMethod = GeneticAlgorithm.tournamentSelect,
        mutationMethod = GeneticAlgorithm.chromosomeMutation,
        crossoverMethod = GeneticAlgorithm.uniformCrossover,
        chromosomeMutationRate = 0.2,
        tournamentSize = 5,
        #geneMutationRate = 0.01,
    )

    GA.run()

    return path.makePath(None)


# Obtém lista de posições válidas
# Posição inicial estará sempre no índice 0
# Posição final estará sempre no índice -1
def listValidPositions(regions, start, goal):
    # Máscara considera apenas os pontos acessíveis
    mask = regions == regions[start]
    mask[start] = False
    mask[goal] = False

    validPositions = mask.nonzero()
    validPositions = list(zip(*validPositions))

    validPositions.append(goal)
    validPositions.insert(0, start)

    return tuple(np.array(validPositions).T)
