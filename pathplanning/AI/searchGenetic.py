from .include import GeneticAlgorithm
from . import preprocess
from . import straight
from . import cost
from . import path

import numpy as np
import numba as nb


__all__ = ['iterativeGeneticSearch']


@nb.njit(
    nb.int64[:](
        nb.int32[:, :],
        nb.types.UniTuple(nb.int64[:], 2),
        nb.boolean[:, :]
    ), parallel = True)
def fit(idx, positions, mask):
    fitness = np.zeros(idx.shape[1], dtype=nb.int64)

    x, y = positions # Posições válidas

    for j in nb.prange(fitness.size):
        c1 = cost.manhattanDistance((x[0], y[0]), (x[idx[0, j]], y[idx[0, j]]))
        c2 = cost.manhattanDistance((x[idx[-1, j]], y[idx[-1, j]]), (x[-1], y[-1]))

        if not straight.checkStraightLine((x[0], y[0]), (x[idx[0, j]], y[idx[0, j]]), mask):
            c1 *= 2

        if not straight.checkStraightLine((x[idx[-1, j]], y[idx[-1, j]]), (x[-1], y[-1]), mask):
            c2 *= 2

        fitness[j] += c1 + c2

    for j in nb.prange(idx.shape[1]):
        for i in nb.prange(idx.shape[0] - 1):
            c =  cost.manhattanDistance((x[idx[i, j]], y[idx[i, j]]), (x[idx[i + 1, j]], y[idx[i + 1, j]]))

            if not straight.checkStraightLine((x[idx[i, j]], y[idx[i, j]]), (x[idx[i + 1, j]], y[idx[i + 1, j]]), mask):
                c *= 2
            
            fitness[j] += c

    return fitness


def iterativeGeneticSearch(start, goal, field, actions, limit = 50):
    # Tentativa 0 (Linha reta)
    if straight.checkStraightLine(start, goal, field.mask):
        return straight.straightLine(start, goal, field, actions)

    # Obtém regiões do mapa
    regions = preprocess.connectedComponentLabeling(field.mask)
    regions = regions == regions[start]
    
    # Verifica se os pontos são acessíveis
    if not regions[goal]:
        return path.makePath(None)

    # Obtém posições válidas
    validPositions = listValidPositions(regions, start, goal)

    # Configuração do algoritmo genético
    threshold = cost.manhattanDistance(start, goal) * 1.50 # Valor para encerrar algoritmo
    populationSize = 200    # Número de indivíduos

    # Algoritmo Genético
    for i in range(limit):
        maxIteractions = i * 100    # Número de interações

        GA = GeneticAlgorithm(
            # Função a ser minimizada
            fitnessFunction = fit,
            arg = validPositions,
            mask = regions,
            lowerBound = 1,
            upperBound = validPositions[0].size - 1,

            # Parâmetros de ajuste do GA
            geneSize = i + 1,
            maxIteractions = maxIteractions,
            populationSize = populationSize,
            threshold = threshold,

            # Parâmetros de ajustes dos métodos
            selectionMethod = GeneticAlgorithm.tournamentSelect,
            mutationMethod = GeneticAlgorithm.chromosomeMutation,
            crossoverMethod = GeneticAlgorithm.uniformCrossover,
            eliteSize = populationSize // 20,
            tournamentSize = populationSize // 10,
            chromosomeMutationRate = 0.2,
            #geneMutationRate = 0.01,
        )

        points, value = GA.run()
        print(value)

        if value <= threshold:
            break

    #print((validPositions[0][points], validPositions[1][points]))

    return path.connectPoints(start, goal, field, actions,
            (validPositions[0][points], validPositions[1][points]))


# Obtém lista de posições válidas
# Posição inicial estará sempre no índice 0
# Posição final estará sempre no índice -1
def listValidPositions(mask, start, goal):
    # Máscara considera apenas os pontos acessíveis
    mask[start] = False
    mask[goal] = False

    validPositions = mask.nonzero()
    validPositions = list(zip(*validPositions))

    validPositions.append(goal)
    validPositions.insert(0, start)

    return tuple(np.array(validPositions).T)
